"""Medical profile: the record that makes a returning visit short."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestContent:
    def test_sections_are_described_for_the_form(self, client: TestClient, api: str):
        response = client.get(f"{api}/patients/me/medical-profile/content")
        assert response.status_code == 200
        from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS

        sections = response.json()["sections"]
        assert len(sections) == len(MEDICAL_PROFILE_SECTIONS)
        for section in sections:
            assert set(section["title"]) == {"en", "hi", "mr", "ta", "gu", "pa"}
            assert set(section["prompt"]) == {"en", "hi", "mr", "ta", "gu", "pa"}

    def test_section_keys_match_the_database_columns(self, client: TestClient, api: str):
        from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS

        sections = client.get(f"{api}/patients/me/medical-profile/content").json()["sections"]
        assert {s["key"] for s in sections} == set(MEDICAL_PROFILE_SECTIONS)

    def test_allergies_are_marked_important(self, client: TestClient, api: str):
        sections = client.get(f"{api}/patients/me/medical-profile/content").json()["sections"]
        allergies = [s for s in sections if s["key"] == "allergies"][0]
        assert allergies.get("important") is True


class TestSaving:
    def test_an_empty_profile_reads_back_as_empty_sections(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812340101")
        body = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        assert body["total_items"] == 0
        assert body["sections"]["allergies"] == []

    def test_saves_items_with_patient_provenance(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812340102")
        body = client.put(
            f"{api}/patients/me/medical-profile",
            json={
                "sections": {
                    "past_medical_history": [{"value": "Type 2 diabetes", "note": "since 2019"}],
                    "allergies": [{"value": "Penicillin"}],
                    "current_medications": [
                        {
                            "value": "Metformin",
                            "attributes": {"dose": "500 mg", "frequency": "Twice daily"},
                        }
                    ],
                }
            },
            headers=headers,
        ).json()

        assert body["total_items"] == 3
        diabetes = body["sections"]["past_medical_history"][0]
        assert diabetes["value"] == "Type 2 diabetes"
        assert diabetes["note"] == "since 2019"
        # Everything the patient says about themselves is patient-sourced,
        # full confidence, and not yet clinician-verified.
        assert diabetes["source"] == "patient"
        assert diabetes["confidence"] == 1.0
        assert diabetes["verified"] is False
        assert diabetes["recorded_at"]

        metformin = body["sections"]["current_medications"][0]
        assert metformin["attributes"] == {"dose": "500 mg", "frequency": "Twice daily"}

    def test_omitted_sections_are_left_untouched(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812340103")
        client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "Penicillin"}]}},
            headers=headers,
        )
        body = client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"family_history": [{"value": "Mother has diabetes"}]}},
            headers=headers,
        ).json()
        assert len(body["sections"]["allergies"]) == 1
        assert len(body["sections"]["family_history"]) == 1

    def test_a_supplied_section_is_replaced_wholesale(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812340104")
        client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "Penicillin"}, {"value": "Aspirin"}]}},
            headers=headers,
        )
        body = client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "Penicillin"}]}},
            headers=headers,
        ).json()
        assert [item["value"] for item in body["sections"]["allergies"]] == ["Penicillin"]

    def test_whitespace_is_tidied(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812340105")
        body = client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "  Sulfa    drugs  "}]}},
            headers=headers,
        ).json()
        assert body["sections"]["allergies"][0]["value"] == "Sulfa drugs"

    def test_an_unknown_section_is_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812340106")
        response = client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"astrological_history": [{"value": "Leo"}]}},
            headers=headers,
        )
        assert response.status_code == 422
        assert "astrological_history" in response.json()["error"]["message"]

    def test_saving_advances_onboarding_to_complete(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812340107")
        # Walk the patient to the medical-profile step.
        client.post(f"{api}/patients/me/abha/skip", headers=headers)
        client.patch(
            f"{api}/patients/me",
            json={"full_name": "Test Patient", "date_of_birth": "1990-01-01", "gender": "female"},
            headers=headers,
        )
        client.post(
            f"{api}/accessibility/assessment",
            json={
                "digital_comfort": "very_comfortable",
                "preferred_interaction": "touching",
                "reading_difficulty": "none",
                "hearing_difficulty": "none",
                "vision_difficulty": "none",
            },
            headers=headers,
        )
        client.put(
            f"{api}/accessibility/preferences",
            json={"accepted_recommendation": True},
            headers=headers,
        )
        client.post(
            f"{api}/consents",
            json={
                "decisions": [
                    {"purpose": "health_data_collection", "granted": True},
                    {"purpose": "share_with_treating_doctor", "granted": True},
                ]
            },
            headers=headers,
        )
        body = client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "No known allergies"}]}},
            headers=headers,
        ).json()
        assert body["onboarding_status"] == "completed"

    def test_requires_authentication(self, client: TestClient, api: str):
        assert client.get(f"{api}/patients/me/medical-profile").status_code == 401
