"""A Hindi patient must not meet English anywhere the interface speaks.

This walks the real API as the Hindi-speaking demo patient and fails on any
Latin-script text that a client would render as words. It is deliberately a
whole-surface sweep rather than a per-endpoint assertion: the failures this
catches are always somewhere nobody thought to look — a raw enum, a status,
a sentence baked into data, a fragment that never got a Hindi form.

Latin text is legitimate in three places, so those are excluded by name:

- machine values the client labels itself (`status`, `document_type`, …),
- text quoted from a document, which is written in whatever language the
  hospital printed it in — usually English, and translating it would be a
  falsification of the record,
- proper nouns and lab names that Hindi also writes in Latin (ABDM, HbA1c).
"""

from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

from tests.test_returning_patient import seed_returning, sign_in_demo

LATIN_WORD = re.compile(r"[A-Za-z]{3,}")

# Fields carrying machine values, identifiers, or text quoted from a document.
# Keyed by field name: the point is to name what is exempt, not to whitelist
# individual strings, so a new English string in a rendered field still fails.
NOT_RENDERED_AS_WORDS = {
    # Identifiers and codes.
    "id", "session_id", "patient_id", "document_id", "encounter_id", "demo_key",
    "abha_id", "abha_address", "access_token", "token_type", "mobile_number",
    "next_route", "route", "instance_key", "question_id", "key", "code",
    "field", "icon", "extractor", "ocr_engine", "provider", "term",
    # Enums the client turns into labels (see frontend `enumLabels.ts`).
    "status", "verification_status", "processing_status", "document_type",
    "type", "source", "note", "flag", "gender", "language", "kind",
    "preferred_language", "answer_kind", "interface_mode", "font_size",
    "contrast_mode", "purpose", "interaction_preference", "care_system",
    "preferred_care_system", "section", "current_section", "priority",
    "visit_type", "red_flag_status", "category", "narrative_source", "state",
    "review_state", "entity_type", "onboarding_status", "event_type",
    "input_method", "detail_kind", "source_kind", "missing", "group",
    "missing_sections", "preference_source",
    # The narrative quotes the record verbatim, so it inherits whatever
    # language the documents were written in. Its own fragments are pinned
    # in `test_i18n.py::TestPatientFacingProseIsLocalised` instead.
    "narrative",
    # Quoted from a document or from the patient's own records. `letterhead`
    # is the clinic, doctor and department read off a printed letterhead — it
    # is the document's own wording, so it stays in the document's language.
    "letterhead",
    "ocr_text", "raw_text", "extracted_text", "text", "attributes", "unit",
    "numeric_value", "reference_range", "file_name", "mime_type", "title",
    "source_name", "note_source", "detail",
    # Names, which are not translated.
    "name", "full_name", "relationship",
    # Sibling translations inside a localised value.
    "en", "mr", "ta", "gu", "pa",
}

# Latin text that is correct inside Hindi prose: proper nouns, and lab names
# that Indian clinical Hindi also writes in Latin.
ALLOWED_LATIN = re.compile(r"ABDM|ABHA|HbA1c|MediKiosk|AI|OD|SOS|BD|TDS")

# `value` is rendered where it holds a clinical item, and machine-only where
# it is an option the patient taps — the label is what they read. So this one
# is exempted by position rather than by name.
MACHINE_BY_POSITION = re.compile(r"_?options\[\d+\]\.value$")


def quoted_from_a_document(node: dict) -> bool:
    """True for a clinical entry read out of a document.

    Its text is the document's own wording. Translating it would misrepresent
    the record, so English there is correct — a district hospital note is
    written in English even for a Hindi-speaking patient.
    """
    return bool(node.get("document_id")) or node.get("source") == "document"


def english_in(node, path: str, out: list[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        exempt = set(NOT_RENDERED_AS_WORDS)
        if quoted_from_a_document(node) or "extractor" in node:
            exempt.add("value")
        for key, value in node.items():
            if key not in exempt:
                english_in(value, f"{path}.{key}", out)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            english_in(value, f"{path}[{index}]", out)
    elif isinstance(node, str):
        if MACHINE_BY_POSITION.search(path):
            return
        remainder = ALLOWED_LATIN.sub("", node)
        if LATIN_WORD.search(remainder):
            out.append((path, node))


READ_ONLY = (
    "/auth/me",
    "/patients/me",
    "/patients/me/profile",
    "/patients/me/home",
    "/patients/me/abha",
    "/patients/me/documents",
    "/patients/me/medical-profile",
    "/patients/me/medical-profile/content",
    "/patients/me/medical-profile/structured",
    "/timeline",
    "/accessibility/content",
    "/accessibility/preferences",
    "/accessibility/recommendation",
    "/consents",
    "/consents/content",
    "/ayush",
    "/ayush/content",
)


@pytest.fixture()
def hindi_patient(client: TestClient, api: str, db) -> dict:
    # Kamla Devi: Hindi, returning, with a visit and a processed document.
    seed_returning(db, "easy")
    return sign_in_demo(client, api, "easy")


class TestNothingEnglishReachesAHindiPatient:
    def test_the_read_only_screens(self, client: TestClient, api: str, hindi_patient):
        findings: list[tuple[str, str]] = []
        for url in READ_ONLY:
            response = client.get(f"{api}{url}", headers=hindi_patient)
            assert response.status_code == 200, (url, response.status_code)
            english_in(response.json(), url, findings)
        assert findings == [], "\n".join(f"{p}: {t[:120]}" for p, t in findings)

    def test_the_whole_visit_and_its_review(
        self, client: TestClient, api: str, hindi_patient
    ):
        findings: list[tuple[str, str]] = []
        started = client.post(f"{api}/encounters/start", json={}, headers=hindi_patient).json()
        encounter_id = started["encounter_id"]
        english_in(started, "start", findings)

        # Choose Ayurveda, so the AYUSH examinations are audited too.
        view = client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": "e_care_system", "text": "ayurveda"},
            headers=hindi_patient,
        ).json()
        for _ in range(60):
            question = view.get("question")
            if not question:
                break
            english_in(question, f"q:{question['id']}", findings)
            options = question.get("options") or []
            text = options[0]["value"] if options else "घुटनों में दर्द"
            view = client.post(
                f"{api}/encounters/{encounter_id}/answer",
                json={"instance_key": question["instance_key"], "text": text},
                headers=hindi_patient,
            ).json()
        else:
            raise AssertionError("visit did not terminate")

        for url in (f"/encounters/{encounter_id}", f"/encounters/{encounter_id}/review"):
            english_in(client.get(f"{api}{url}", headers=hindi_patient).json(), url, findings)
        assert findings == [], "\n".join(f"{p}: {t[:120]}" for p, t in findings)

    def test_the_visit_narrative_is_hindi_prose(
        self, client: TestClient, api: str, hindi_patient
    ):
        """The one screen the patient reads as a paragraph before submitting."""
        started = client.post(f"{api}/encounters/start", json={}, headers=hindi_patient).json()
        encounter_id = started["encounter_id"]
        client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": "e_care_system", "text": "allopathy"},
            headers=hindi_patient,
        )
        client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": "e_complaint", "text": "घुटनों में दर्द"},
            headers=hindi_patient,
        )
        review = client.get(
            f"{api}/encounters/{encounter_id}/review", headers=hindi_patient
        ).json()
        narrative = review["narrative"]
        assert "घुटनों में दर्द" in narrative
        # The safety wording has to survive localisation.
        assert "निदान नहीं" in narrative
