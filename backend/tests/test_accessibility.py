"""Accessibility assessment, recommendation and preference customisation."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.shared.enums import Language

COMFORTABLE = {
    "digital_comfort": "very_comfortable",
    "preferred_interaction": "touching",
    "reading_difficulty": "none",
    "hearing_difficulty": "none",
    "vision_difficulty": "none",
}
NEEDS_SIMPLE = {**COMFORTABLE, "digital_comfort": "prefer_simple"}
LOW_VISION = {**COMFORTABLE, "vision_difficulty": "yes", "reading_difficulty": "yes"}


class TestContent:
    def test_questions_are_served_with_every_language(self, client: TestClient, api: str):
        response = client.get(f"{api}/accessibility/content")
        assert response.status_code == 200
        body = response.json()
        assert len(body["questions"]) == 6

        fields = {question["field"] for question in body["questions"]}
        assert fields == {
            "digital_comfort",
            "preferred_interaction",
            "reading_difficulty",
            "hearing_difficulty",
            "vision_difficulty",
            "additional_needs",
        }
        for question in body["questions"]:
            assert set(question["prompt"]) == {"en", "hi", "mr", "ta", "gu", "pa"}
            for option in question["options"]:
                assert set(option["label"]) == {"en", "hi", "mr", "ta", "gu", "pa"}

    def test_only_the_optional_question_is_not_required(self, client: TestClient, api: str):
        questions = client.get(f"{api}/accessibility/content").json()["questions"]
        optional = [q["field"] for q in questions if not q["required"]]
        assert optional == ["additional_needs"]


class TestAssessment:
    def test_requires_authentication(self, client: TestClient, api: str):
        assert client.post(f"{api}/accessibility/assessment", json=COMFORTABLE).status_code == 401

    def test_comfortable_patient_gets_the_standard_experience(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320001")
        response = client.post(
            f"{api}/accessibility/assessment", json=COMFORTABLE, headers=headers
        )
        assert response.status_code == 200
        body = response.json()
        assert body["recommendation"]["interface_mode"] == "standard"
        assert body["recommendation"]["font_size"] == "normal"
        assert body["preferences"]["source"] == "recommended"
        assert body["next_route"] == "/onboarding/preferences"

    def test_patient_who_wants_simple_gets_easy_mode(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320002")
        body = client.post(
            f"{api}/accessibility/assessment", json=NEEDS_SIMPLE, headers=headers
        ).json()
        assert body["recommendation"]["interface_mode"] == "easy"
        assert body["recommendation"]["font_size"] in ("large", "extra_large")

    def test_low_vision_gets_large_text_and_high_contrast(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320003")
        body = client.post(
            f"{api}/accessibility/assessment", json=LOW_VISION, headers=headers
        ).json()
        assert body["recommendation"]["font_size"] == "extra_large"
        assert body["recommendation"]["contrast_mode"] == "high"
        assert body["recommendation"]["audio_guidance"] is True

    def test_hearing_difficulty_never_depends_on_audio(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320004")
        body = client.post(
            f"{api}/accessibility/assessment",
            json={**LOW_VISION, "hearing_difficulty": "yes"},
            headers=headers,
        ).json()
        assert body["recommendation"]["audio_guidance"] is False

    def test_the_patient_is_told_why(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320005")
        body = client.post(
            f"{api}/accessibility/assessment", json=LOW_VISION, headers=headers
        ).json()
        reasons = body["recommendation"]["reasons"]
        assert reasons
        assert all(reason["en"] and reason["hi"] for reason in reasons)

    def test_optional_needs_are_not_required(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320006")
        response = client.post(
            f"{api}/accessibility/assessment", json=COMFORTABLE, headers=headers
        )
        assert response.status_code == 200

    def test_voluntary_needs_influence_the_result(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320007")
        body = client.post(
            f"{api}/accessibility/assessment",
            json={**COMFORTABLE, "additional_needs": ["low_literacy"]},
            headers=headers,
        ).json()
        assert body["recommendation"]["interface_mode"] == "easy"

    def test_an_invalid_answer_is_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320008")
        response = client.post(
            f"{api}/accessibility/assessment",
            json={**COMFORTABLE, "digital_comfort": "extremely_comfortable"},
            headers=headers,
        )
        assert response.status_code == 422

    def test_the_recommendation_snapshot_is_retrievable(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320009")
        assert client.get(f"{api}/accessibility/recommendation", headers=headers).json() is None
        client.post(f"{api}/accessibility/assessment", json=NEEDS_SIMPLE, headers=headers)
        snapshot = client.get(f"{api}/accessibility/recommendation", headers=headers).json()
        assert snapshot["interface_mode"] == "easy"
        assert snapshot["easy_mode_score"] >= snapshot["easy_mode_threshold"]


class TestPreferences:
    def test_defaults_exist_before_the_assessment(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320020")
        body = client.get(f"{api}/accessibility/preferences", headers=headers).json()
        assert body["interface_mode"] == "standard"
        assert body["font_size"] == "normal"
        assert body["audio_guidance"] is False

    def test_accepting_the_recommendation_keeps_it_marked_recommended(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320021")
        client.post(f"{api}/accessibility/assessment", json=NEEDS_SIMPLE, headers=headers)
        body = client.put(
            f"{api}/accessibility/preferences",
            json={"accepted_recommendation": True},
            headers=headers,
        ).json()
        assert body["source"] == "recommended"
        assert body["interface_mode"] == "easy"

    def test_customising_is_recorded_as_customised(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320022")
        client.post(f"{api}/accessibility/assessment", json=NEEDS_SIMPLE, headers=headers)
        body = client.put(
            f"{api}/accessibility/preferences",
            json={"interface_mode": "standard", "accepted_recommendation": False},
            headers=headers,
        ).json()
        assert body["source"] == "customized"
        assert body["interface_mode"] == "standard"

    def test_a_patient_is_never_locked_into_a_mode(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812320023")
        client.post(f"{api}/accessibility/assessment", json=NEEDS_SIMPLE, headers=headers)
        client.put(
            f"{api}/accessibility/preferences",
            json={"accepted_recommendation": True},
            headers=headers,
        )
        # Change it again later — still allowed.
        for mode in ("standard", "easy", "standard"):
            body = client.put(
                f"{api}/accessibility/preferences",
                json={"interface_mode": mode, "accepted_recommendation": False},
                headers=headers,
            ).json()
            assert body["interface_mode"] == mode

    def test_changing_language_updates_the_patient_record(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320024")
        client.put(
            f"{api}/accessibility/preferences",
            json={"language": "hi", "accepted_recommendation": False},
            headers=headers,
        )
        patient = client.get(f"{api}/patients/me", headers=headers).json()
        assert patient["preferred_language"] == "hi"

    def test_confirming_preferences_advances_onboarding(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812320025")
        client.post(f"{api}/accessibility/assessment", json=COMFORTABLE, headers=headers)
        client.put(
            f"{api}/accessibility/preferences",
            json={"accepted_recommendation": True},
            headers=headers,
        )
        patient = client.get(f"{api}/patients/me", headers=headers).json()
        assert patient["onboarding_status"] == "consent_pending"


class TestEveryLanguageCanBePersisted:
    """A language the interface offers must be storable.

    The four regional languages were added to `Language` long before the
    PostgreSQL ENUM type learned about them. Tests build their schema from the
    models, so the type had all six values here and the gap was invisible —
    while on a migrated database persisting one of them failed, and the patient
    saw their language silently revert. This test would still not have caught
    the ENUM itself, so `test_migrations.py` checks that separately; this one
    guards the round trip through the API.
    """

    @pytest.mark.parametrize("language", [lang.value for lang in Language])
    def test_it_round_trips_through_the_api(
        self, client: TestClient, api: str, sign_in, language: str
    ):
        headers, _ = sign_in("9812430077")
        response = client.put(
            f"{api}/accessibility/preferences",
            json={"language": language, "accepted_recommendation": False},
            headers=headers,
        )
        assert response.status_code == 200, response.text
        assert response.json()["language"] == language
        # And the patient's language of record follows the interface.
        assert client.get(f"{api}/patients/me", headers=headers).json()[
            "preferred_language"
        ] == language
