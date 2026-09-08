"""Encounter summary: today's report set against relevant history.

Three provenance classes are kept distinct all the way to the UI:
`patient` (said today), `document` (read from a scan) and `previous_record`
(known from earlier visits). Nothing is merged into a single undifferentiated
list, because a clinician needs to know which is which.

No diagnosis, no certainty language — see the narrative template.
"""

from __future__ import annotations

import logging
import re

from sqlalchemy.orm import Session

from app.modules.encounter.models import Encounter
from app.modules.medical_history import service as medical_service
from app.modules.medical_history.structured import SECTION_LABELS
from app.modules.patient.models import Patient
from app.services.ai import get_provider, structured
from app.services.ai import prompts
from app.services.ai.schemas import HistorySummary
from app.shared.enums import Language, RedFlagStatus
from app.shared.i18n import GENDER_LABELS, Localised, enum_label, localise, t

log = logging.getLogger("medikiosk.encounter.summary")

NONE_REPORTED = "None reported"

# Recognises a stored severity answer such as "7/10".
SEVERITY_PATTERN = re.compile(r"^\d{1,2}/10$")

DISCLAIMER: Localised = t(
    "This records what you told us today alongside what we already knew. "
    "It is not a diagnosis, and a healthcare professional will review it with you.",
    "यह आज आपने जो बताया और जो हमें पहले से ज्ञात था, उसका रिकॉर्ड है। "
    "यह निदान नहीं है, और कोई स्वास्थ्य पेशेवर इसे आपके साथ देखेगा।",
)

# The narrative is the patient's last look at what goes to the doctor, so it
# is assembled from localised fragments. Each fragment is a whole clause: Hindi
# will not survive word-by-word substitution into an English sentence.
_COPY: dict[str, Localised] = {
    "years_old": t("{age}-year-old", "{age} वर्ष"),
    "the_patient": t("The patient", "मरीज़"),
    # Phrased as "the complaint is" so no fragment needs a gendered verb.
    "presents": t(
        "{subject} presents reporting: {complaint}.",
        "{subject} की शिकायत: {complaint}।",
    ),
    "returns": t(
        "{subject} returns reporting: {complaint}.",
        "{subject} फिर आए हैं, शिकायत: {complaint}।",
    ),
    "unspecified": t("an unspecified concern", "कोई अस्पष्ट परेशानी"),
    "hpi": t("About this problem today: {items}.", "आज इस समस्या के बारे में: {items}।"),
    "severity": t(
        "Severity reported by the patient: {value}.",
        "मरीज़ द्वारा बताई गई गंभीरता: {value}।",
    ),
    "no_detail": t(
        "No further detail was given about the problem.",
        "समस्या के बारे में इससे अधिक जानकारी नहीं दी गई।",
    ),
    "ros": t("Also reported today: {items}.", "आज यह भी बताया: {items}।"),
    "known_conditions": t(
        "Known conditions from earlier visits: {items}.",
        "पिछली मुलाक़ातों से ज्ञात स्थितियाँ: {items}।",
    ),
    "medications": t("Medications on record: {items}.", "रिकॉर्ड में दवाइयाँ: {items}।"),
    "allergies": t("Allergies on record: {items}.", "रिकॉर्ड में एलर्जी: {items}।"),
    "no_allergies": t("No allergies recorded.", "कोई एलर्जी दर्ज नहीं है।"),
    "new_medications": t(
        "Medication changes reported today: {items}.",
        "आज बताए गए दवा में बदलाव: {items}।",
    ),
    "new_conditions": t(
        "New conditions reported today: {items}.",
        "आज बताई गई नई स्थितियाँ: {items}।",
    ),
    "urgent": t(
        "This visit has been marked urgent because some described symptoms "
        "may require prompt attention.",
        "इस मुलाक़ात को तत्काल चिह्नित किया गया है क्योंकि बताए गए कुछ लक्षणों पर "
        "शीघ्र ध्यान देने की आवश्यकता हो सकती है।",
    ),
    "closing": t(
        "Recorded from the patient's own account and their existing records. "
        "This is not a diagnosis.",
        "यह मरीज़ के स्वयं के बताए अनुसार और उनके मौजूदा रिकॉर्ड से दर्ज किया गया है। "
        "यह कोई निदान नहीं है।",
    ),
}

# Sections that should carry something before a visit is useful to a clinician.
EXPECTED_TODAY = ("chief_complaint", "history_of_present_illness")


def _today_values(encounter: Encounter, section: str) -> list[str]:
    return [
        str(entry.get("value", ""))
        for entry in (encounter.structured_history or {}).get(section, [])
        if entry.get("value") and entry.get("value") != NONE_REPORTED
    ]


def missing_today(encounter: Encounter) -> list[str]:
    return [section for section in EXPECTED_TODAY if not _today_values(encounter, section)]


def template_narrative(
    patient: Patient, encounter: Encounter, existing, language: Language | str = Language.ENGLISH
) -> str:
    """Deterministic prose. Always available; never interpretive."""

    def copy(key: str, **fields: str) -> str:
        text = localise(_COPY[key], language)
        for name, value in fields.items():
            text = text.replace("{" + name + "}", value)
        return text

    descriptor = ", ".join(
        part
        for part in (
            copy("years_old", age=str(patient.age)) if patient.age is not None else "",
            enum_label(GENDER_LABELS, patient.gender, language),
        )
        if part
    )
    subject = patient.full_name or copy("the_patient")
    opening = f"{subject} ({descriptor})" if descriptor else subject

    parts: list[str] = []
    complaint = encounter.chief_complaint or ", ".join(_today_values(encounter, "chief_complaint"))
    visit = "returns" if encounter.visit_type.value == "follow_up" else "presents"
    # Quoted as recorded: lower-casing mangles a first-person answer such as
    # "I have crushing chest pain".
    parts.append(
        copy(visit, subject=opening, complaint=complaint or copy("unspecified"))
    )

    # Severity reads as a metric, not as a bare "1/10" among prose fragments.
    hpi_all = _today_values(encounter, "history_of_present_illness")
    severity = next((v for v in hpi_all if SEVERITY_PATTERN.match(v)), None)
    hpi = [v for v in hpi_all if v != severity]
    if hpi:
        parts.append(copy("hpi", items="; ".join(hpi)))
    if severity:
        parts.append(copy("severity", value=severity))
    if not hpi and not severity:
        parts.append(copy("no_detail"))

    ros = _today_values(encounter, "review_of_systems")
    if ros:
        parts.append(copy("ros", items=", ".join(ros)))

    # Existing history is quoted as prior knowledge, not as today's findings.
    if existing.conditions:
        parts.append(copy("known_conditions", items=", ".join(existing.conditions)))
    if existing.medications:
        parts.append(copy("medications", items=", ".join(existing.medications)))
    parts.append(
        copy("allergies", items=", ".join(existing.allergies))
        if existing.allergies
        else copy("no_allergies")
    )

    new_meds = _today_values(encounter, "current_medications")
    if new_meds:
        parts.append(copy("new_medications", items=", ".join(new_meds)))
    new_conditions = _today_values(encounter, "past_medical_history")
    if new_conditions:
        parts.append(copy("new_conditions", items=", ".join(new_conditions)))

    if encounter.red_flag_status == RedFlagStatus.ACTIVE:
        # Hedged deliberately: this is a triage signal, not a finding. The
        # closing sentence below already says "not a diagnosis", so this one
        # does not repeat it.
        parts.append(copy("urgent"))

    parts.append(copy("closing"))
    return " ".join(parts)


async def narrative(
    db: Session, patient: Patient, encounter: Encounter, existing
) -> tuple[str, str]:
    """@returns (text, "template" | "ai")."""
    language = patient.preferred_language
    fallback = template_narrative(patient, encounter, existing, language)

    provider = get_provider()
    if provider.name == "none":
        return fallback, "template"

    profile = medical_service.ensure_profile(db, patient)
    sections = medical_service.read_sections(profile)
    payload = {
        f"TODAY · {SECTION_LABELS.get(name, name)}": _today_values(encounter, name)
        for name in (encounter.structured_history or {})
    }
    payload.update(
        {
            f"ON RECORD · {SECTION_LABELS.get(name, name)}": [
                item.value for item in items if item.value != NONE_REPORTED
            ]
            for name, items in sections.items()
            if items
        }
    )

    system, prompt = prompts.summarise_history(sections=payload)
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=1200)
    except Exception as exc:  # noqa: BLE001
        log.warning("encounter summary generation failed: %s", exc)
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
    return (text.strip() or fallback), "ai"
