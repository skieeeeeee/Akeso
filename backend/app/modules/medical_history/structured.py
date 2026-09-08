"""Structured history generation.

Merges what the patient said with what their documents say, keeping the two
clearly labelled. The narrative is written by the AI layer when it is
available and by a deterministic template when it is not — in both cases from
the already-structured data, so the prose can never introduce a fact.

Nothing here diagnoses. Section names are clinical, the content is quotation.
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.ayush import service as ayush_service
from app.modules.documents.models import Document
from app.modules.medical_history import service as medical_service
from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS
from app.modules.patient.models import Patient
from app.services.ai import get_provider, structured
from app.services.ai import prompts
from app.services.ai.schemas import HistorySummary
from app.shared.enums import ExtractedEntityType, Language, ReviewState
from app.shared.i18n import (
    GENDER_LABELS,
    Localised,
    enum_label,
    localise,
    t,
)
from app.shared.clinical import ClinicalItem

log = logging.getLogger("medikiosk.history")

# Which extracted entity type contributes to which history section.
ENTITY_TO_SECTION: dict[ExtractedEntityType, str] = {
    ExtractedEntityType.DIAGNOSIS: "past_medical_history",
    ExtractedEntityType.MEDICATION: "current_medications",
    ExtractedEntityType.INVESTIGATION: "previous_investigations",
    ExtractedEntityType.SURGERY: "surgical_history",
    ExtractedEntityType.PROCEDURE: "surgical_history",
    ExtractedEntityType.ALLERGY: "allergies",
}

# Sections a doctor would expect to see filled in.
EXPECTED_SECTIONS = (
    "chief_complaint",
    "past_medical_history",
    "current_medications",
    "allergies",
)

SECTION_LABELS_LOCALISED: dict[str, Localised] = {
    "chief_complaint": t("Chief complaint", "मुख्य शिकायत"),
    "history_of_present_illness": t("History of present illness", "वर्तमान बीमारी का इतिहास"),
    "past_medical_history": t("Past medical history", "पिछला चिकित्सा इतिहास"),
    "surgical_history": t("Past surgical history", "पिछला शल्य चिकित्सा इतिहास"),
    "current_medications": t("Medications", "दवाइयाँ"),
    "drug_history": t("Drug history", "दवा का इतिहास"),
    "allergies": t("Allergies", "एलर्जी"),
    "family_history": t("Family history", "पारिवारिक इतिहास"),
    "personal_history": t("Personal history", "व्यक्तिगत इतिहास"),
    "previous_investigations": t("Previous investigations", "पिछली जाँचें"),
    "review_of_systems": t("Review of systems", "प्रणालियों की समीक्षा"),
    "additional_information": t("Additional information", "अतिरिक्त जानकारी"),
}


def section_labels(language: Language | str) -> dict[str, str]:
    """Clinical section names in the patient's language."""
    return {
        key: localise(value, language)
        for key, value in SECTION_LABELS_LOCALISED.items()
    }


# The English map is still used to build the AI prompt, which is written in
# English regardless of the patient's language.
SECTION_LABELS: dict[str, str] = {
    key: value["en"] for key, value in SECTION_LABELS_LOCALISED.items()
}

NONE_REPORTED = "None reported"
# Stored sentinel, so it cannot be localised in the database. It is swapped
# for a localised label on the way out, after every internal comparison.
NONE_REPORTED_LABEL = t("None reported", "कुछ नहीं बताया गया")


def _entry(item: ClinicalItem) -> dict:
    return {
        "value": item.value,
        "attributes": item.attributes,
        "source": item.source.value,
        "confidence": item.confidence,
        "verified": item.verified,
        "note": item.note,
        "note_source": "",
        "document_id": item.document_id,
    }


def build(db: Session, patient: Patient) -> dict:
    """Assemble the structured history, source-labelled."""
    profile = medical_service.ensure_profile(db, patient)
    sections: dict[str, list[dict]] = {
        name: [_entry(item) for item in medical_service.read_sections(profile)[name]]
        for name in MEDICAL_PROFILE_SECTIONS
    }
    patient_reported = sum(len(items) for items in sections.values())

    # Document findings are appended, never merged into the patient's own
    # statements — the doctor must be able to tell them apart.
    documents = list(
        db.scalars(
            select(Document)
            .where(Document.patient_id == patient.id)
            .options(selectinload(Document.extracted_items))
        ).all()
    )
    document_derived = 0
    for document in documents:
        label = (document.title or document.file_name).strip()
        for item in document.extracted_items:
            if item.review_state == ReviewState.REJECTED:
                continue
            section = ENTITY_TO_SECTION.get(item.entity_type)
            if section is None:
                continue
            detail = " ".join(
                part
                for part in (item.numeric_value or "", item.unit or "")
                if part
            ).strip()
            sections[section].append(
                {
                    "value": item.value if not detail else f"{item.value} — {detail}",
                    "attributes": dict(item.attributes),
                    "source": "document",
                    "confidence": item.confidence,
                    "verified": item.review_state == ReviewState.ACCEPTED,
                    "note": "found_in_document",
                    "note_source": label,
                    "document_id": str(document.id),
                    "flag": item.flag.value if item.flag else None,
                }
            )
            document_derived += 1

    missing = [
        name
        for name in EXPECTED_SECTIONS
        if not [
            entry
            for entry in sections[name]
            if entry["value"] != NONE_REPORTED
        ]
    ]

    ayush = ayush_service.get(db, patient)

    return {
        "sections": sections,
        "labels": SECTION_LABELS,
        "patient_reported_count": patient_reported,
        "document_derived_count": document_derived,
        "missing_sections": missing,
        "ayush_included": ayush is not None and bool(ayush.dashavidha),
    }


# The narrative is read by the patient before it goes to the doctor, so it is
# assembled from localised fragments rather than translated after the fact.
_NARRATIVE_LEADS: tuple[tuple[str, Localised], ...] = (
    ("history_of_present_illness", t("Regarding this problem", "इस समस्या के बारे में")),
    ("past_medical_history", t("Past medical history", "पिछला चिकित्सा इतिहास")),
    ("surgical_history", t("Past surgical history", "पिछला शल्य चिकित्सा इतिहास")),
    ("current_medications", t("Current medications", "वर्तमान दवाइयाँ")),
    ("allergies", t("Allergies", "एलर्जी")),
    ("family_history", t("Family history", "पारिवारिक इतिहास")),
    ("personal_history", t("Personal history", "व्यक्तिगत इतिहास")),
    ("previous_investigations", t("Previous investigations", "पिछली जाँचें")),
    ("review_of_systems", t("Also reports", "यह भी बताया")),
)

_NARRATIVE_COPY = {
    "years_old": t("{age}-year-old", "{age} वर्ष"),
    "the_patient": t("The patient", "मरीज़"),
    # Phrased as "complaint of X" rather than "reports X" so the sentence
    # needs no gendered verb in Hindi.
    "complaint_of": t("{subject} reports: {complaint}.", "{subject} की शिकायत: {complaint}।"),
    "no_complaint": t("no specific complaint", "कोई विशेष शिकायत नहीं"),
    "section": t("{lead}: {found}.", "{lead}: {found}।"),
    "section_empty": t("{lead}: none reported.", "{lead}: कुछ नहीं बताया गया।"),
    "disclaimer": t(
        "This is a record of information provided by the patient and read from "
        "their documents. It is not a diagnosis.",
        "यह मरीज़ द्वारा दी गई और उनके दस्तावेज़ों से पढ़ी गई जानकारी का रिकॉर्ड है। "
        "यह कोई निदान नहीं है।",
    ),
}


def _template_narrative(
    patient: Patient,
    sections: dict[str, list[dict]],
    language: Language | str,
) -> str:
    """Deterministic prose. Always available, never interpretive."""

    def copy(key: str) -> str:
        return localise(_NARRATIVE_COPY[key], language)

    def values(name: str) -> list[str]:
        return [
            entry["value"]
            for entry in sections.get(name, [])
            if entry["value"] != NONE_REPORTED
        ]

    # Build the descriptor from whatever we actually know, so a patient with
    # no name or gender recorded does not read as "New patient, patient".
    descriptor = ", ".join(
        part
        for part in (
            copy("years_old").replace("{age}", str(patient.age))
            if patient.age is not None
            else "",
            enum_label(GENDER_LABELS, patient.gender, language),
        )
        if part
    )
    subject = patient.full_name or copy("the_patient")
    opening = f"{subject} ({descriptor})" if descriptor else subject

    complaint = values("chief_complaint")
    parts: list[str] = [
        copy("complaint_of")
        .replace("{subject}", opening)
        .replace(
            "{complaint}",
            ", ".join(complaint) if complaint else copy("no_complaint"),
        )
    ]
    for name, lead in _NARRATIVE_LEADS:
        found = values(name)
        label = localise(lead, language)
        parts.append(
            copy("section").replace("{lead}", label).replace("{found}", "; ".join(found))
            if found
            else copy("section_empty").replace("{lead}", label)
        )

    parts.append(copy("disclaimer"))
    return " ".join(parts)


def for_display(history: dict, language: Language | str) -> dict:
    """Swap stored sentinels for localised labels on the way to the client."""
    label = localise(NONE_REPORTED_LABEL, language)
    for entries in history["sections"].values():
        for entry in entries:
            if entry["value"] == NONE_REPORTED:
                entry["value"] = label
    return history


async def narrative(db: Session, patient: Patient, history: dict) -> tuple[str, str]:
    """@returns (text, source) where source is "template" or "ai"."""
    sections = history["sections"]
    language = patient.preferred_language
    fallback = _template_narrative(patient, sections, language)

    provider = get_provider()
    if provider.name == "none":
        return fallback, "template"

    plain = {
        SECTION_LABELS.get(name, name): [entry["value"] for entry in entries]
        for name, entries in sections.items()
        if entries
    }
    system, prompt = prompts.summarise_history(sections=plain)
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=1200)
    except Exception as exc:  # noqa: BLE001 - prose is never worth a failure
        log.warning("summary generation failed: %s", exc)
        return fallback, "template"

    parsed = structured(HistorySummary, raw)
    if parsed is None:
        return fallback, "template"
    # Any non-English language prefers the Hindi summary, matching the
    # fallback chain: Hindi is closer than English for every one of them.
    text = (
        parsed.summary_hi
        if language != Language.ENGLISH and parsed.summary_hi
        else parsed.summary_en
    )
    return text.strip() or fallback, "ai"
