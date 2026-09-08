"""Phase 1 acceptance criteria (spec §22).

Walks the complete first-time journey through the HTTP API and asserts that
every piece of it persists, that the journey can be resumed from any point,
and that a returning patient is recognised and routed correctly.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

COMFORTABLE_ASSESSMENT = {
    "digital_comfort": "somewhat_comfortable",
    "preferred_interaction": "both",
    "reading_difficulty": "none",
    "hearing_difficulty": "none",
    "vision_difficulty": "none",
}
REQUIRED_CONSENTS = {
    "decisions": [
        {"purpose": "health_data_collection", "granted": True},
        {"purpose": "share_with_treating_doctor", "granted": True},
        {"purpose": "abha_linkage", "granted": True},
    ]
}


def complete_journey(client: TestClient, api: str, mobile: str, language: str = "en") -> dict:
    """Run the whole first-time journey and return the auth headers."""
    requested = client.post(
        f"{api}/auth/otp/request", json={"mobile_number": mobile}
    ).json()
    session = client.post(
        f"{api}/auth/otp/verify",
        json={
            "mobile_number": mobile,
            "code": requested["prototype_code"],
            "language": language,
        },
    ).json()
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    client.post(
        f"{api}/patients/me/abha/link",
        json={"abha_id": "12-3456-7890-4321"},
        headers=headers,
    )
    client.patch(
        f"{api}/patients/me",
        json={
            "full_name": "Priya Menon",
            "date_of_birth": "1988-09-14",
            "gender": "female",
            "preferred_language": language,
            "emergency_contact_name": "Arun Menon",
            "emergency_contact_number": "9812399999",
            "emergency_contact_relation": "Spouse",
        },
        headers=headers,
    )
    client.post(
        f"{api}/accessibility/assessment", json=COMFORTABLE_ASSESSMENT, headers=headers
    )
    client.put(
        f"{api}/accessibility/preferences",
        json={"accepted_recommendation": True},
        headers=headers,
    )
    client.post(f"{api}/consents", json=REQUIRED_CONSENTS, headers=headers)
    client.put(
        f"{api}/patients/me/medical-profile",
        json={
            "sections": {
                "past_medical_history": [{"value": "Hypothyroidism", "note": "since 2020"}],
                "current_medications": [
                    {"value": "Levothyroxine", "attributes": {"dose": "50 mcg"}}
                ],
                "allergies": [{"value": "No known allergies"}],
            }
        },
        headers=headers,
    )
    return headers


class TestFirstTimeJourney:
    def test_each_step_moves_the_patient_forward(self, client: TestClient, api: str):
        mobile = "9812390001"
        requested = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": mobile}
        ).json()
        session = client.post(
            f"{api}/auth/otp/verify",
            json={"mobile_number": mobile, "code": requested["prototype_code"]},
        ).json()
        headers = {"Authorization": f"Bearer {session['access_token']}"}

        # The server, not the client, decides where the patient goes next.
        assert session["onboarding"]["next_route"] == "/onboarding/abha"

        steps = [
            (
                lambda: client.post(
                    f"{api}/patients/me/abha/link",
                    json={"abha_id": "12-3456-7890-4321"},
                    headers=headers,
                ),
                "/onboarding/personal",
            ),
            (
                lambda: client.patch(
                    f"{api}/patients/me",
                    json={
                        "full_name": "Priya Menon",
                        "date_of_birth": "1988-09-14",
                        "gender": "female",
                    },
                    headers=headers,
                ),
                "/onboarding/assessment",
            ),
            (
                lambda: client.post(
                    f"{api}/accessibility/assessment",
                    json=COMFORTABLE_ASSESSMENT,
                    headers=headers,
                ),
                "/onboarding/preferences",
            ),
            (
                lambda: client.put(
                    f"{api}/accessibility/preferences",
                    json={"accepted_recommendation": True},
                    headers=headers,
                ),
                "/onboarding/consent",
            ),
            (
                lambda: client.post(f"{api}/consents", json=REQUIRED_CONSENTS, headers=headers),
                "/onboarding/medical-profile",
            ),
            (
                lambda: client.put(
                    f"{api}/patients/me/medical-profile",
                    json={"sections": {"allergies": [{"value": "No known allergies"}]}},
                    headers=headers,
                ),
                "/profile",
            ),
        ]

        for call, expected_route in steps:
            response = call()
            assert response.status_code in (200, 201), response.text
            actual = client.get(f"{api}/auth/me", headers=headers).json()
            assert actual["onboarding"]["next_route"] == expected_route

        final = client.get(f"{api}/auth/me", headers=headers).json()
        assert final["onboarding"]["is_complete"] is True
        assert final["onboarding"]["percent"] == 100

    def test_everything_persists_in_postgresql(self, client: TestClient, api: str, db):
        headers = complete_journey(client, api, "9812390002", language="hi")

        from sqlalchemy import select

        from app.modules.patient.models import Patient

        patient = db.scalar(select(Patient).where(Patient.mobile_number == "9812390002"))
        assert patient is not None
        # Read straight from the database, not from the API response.
        assert patient.full_name == "Priya Menon"
        assert patient.date_of_birth.isoformat() == "1988-09-14"
        assert patient.age == 37
        assert patient.onboarding_status.value == "completed"
        assert patient.emergency_contact_name == "Arun Menon"

        assert patient.abha_profile.verification_status.value == "verified"
        assert patient.abha_profile.is_mock is True

        assert patient.preferences is not None
        assert patient.preferences.interface_mode.value == "standard"

        assert len(patient.assessments) == 1
        assert patient.assessments[0].recommendation["interface_mode"] == "standard"
        assert patient.assessments[0].age_at_assessment == 37

        granted = {c.purpose.value for c in patient.consents if c.is_active}
        assert granted == {
            "health_data_collection",
            "share_with_treating_doctor",
            "abha_linkage",
        }

        assert patient.medical_profile.recorded_item_count == 3

    def test_the_profile_screen_has_real_content(self, client: TestClient, api: str):
        headers = complete_journey(client, api, "9812390003")
        profile = client.get(f"{api}/patients/me/profile", headers=headers).json()

        assert profile["patient"]["full_name"] == "Priya Menon"
        assert profile["patient"]["age"] == 37
        assert profile["abha"]["verification_status"] == "verified"
        assert profile["preferences"]["interface_mode"] == "standard"
        assert len(profile["consents"]) == 3
        assert profile["medical_profile"]["total_items"] == 3
        assert profile["medical_profile"]["sections"]["current_medications"] == 1
        assert profile["last_assessment_at"] is not None
        assert profile["onboarding"]["is_complete"] is True


class TestResumability:
    def test_a_patient_resumes_where_they_stopped(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812390010")
        client.post(f"{api}/patients/me/abha/skip", headers=headers)
        client.patch(
            f"{api}/patients/me",
            json={
                "full_name": "Half Way",
                "date_of_birth": "1995-02-02",
                "gender": "other",
            },
            headers=headers,
        )

        # Sign in again on a "different device".
        fresh_headers, session = sign_in("9812390010")
        assert session["is_new_patient"] is False
        assert session["onboarding"]["next_route"] == "/onboarding/assessment"
        assert session["patient"]["full_name"] == "Half Way"

    def test_progress_is_never_lost_by_revisiting_an_earlier_step(
        self, client: TestClient, api: str
    ):
        headers = complete_journey(client, api, "9812390011")
        assert (
            client.get(f"{api}/auth/me", headers=headers).json()["onboarding"]["is_complete"]
            is True
        )

        # A completed patient edits their name again.
        client.patch(f"{api}/patients/me", json={"full_name": "Priya M Menon"}, headers=headers)
        after = client.get(f"{api}/auth/me", headers=headers).json()
        assert after["onboarding"]["is_complete"] is True
        assert after["patient"]["full_name"] == "Priya M Menon"

    def test_partial_personal_info_is_kept_across_requests(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812390012")
        client.patch(f"{api}/patients/me", json={"full_name": "Slow Typist"}, headers=headers)
        # Nothing else supplied yet, so the step is not finished...
        assert (
            client.get(f"{api}/patients/me", headers=headers).json()["onboarding_status"]
            == "abha_pending"
        )
        # ...but the name survived.
        assert client.get(f"{api}/patients/me", headers=headers).json()["full_name"] == "Slow Typist"


class TestReturningPatient:
    def test_a_completed_patient_is_routed_to_their_profile(self, client: TestClient, api: str):
        complete_journey(client, api, "9812390020")

        requested = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": "9812390020"}
        ).json()
        session = client.post(
            f"{api}/auth/otp/verify",
            json={"mobile_number": "9812390020", "code": requested["prototype_code"]},
        ).json()

        assert session["is_new_patient"] is False
        assert session["onboarding"]["is_complete"] is True
        assert session["onboarding"]["next_route"] == "/profile"

    def test_their_history_is_still_there(self, client: TestClient, api: str):
        headers = complete_journey(client, api, "9812390021")
        profile = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        assert profile["total_items"] == 3
        # This is exactly what spares a returning patient from repeating it.
        assert profile["sections"]["past_medical_history"][0]["value"] == "Hypothyroidism"


class TestEasyModeJourney:
    def test_a_patient_who_needs_easy_mode_gets_it_end_to_end(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812390030", language="hi")
        client.post(f"{api}/patients/me/abha/skip", headers=headers)
        client.patch(
            f"{api}/patients/me",
            json={
                "full_name": "Kamla Devi",
                "date_of_birth": "1952-01-10",
                "gender": "female",
                "preferred_language": "hi",
            },
            headers=headers,
        )
        result = client.post(
            f"{api}/accessibility/assessment",
            json={
                "digital_comfort": "prefer_simple",
                "preferred_interaction": "speaking",
                "reading_difficulty": "sometimes",
                "hearing_difficulty": "none",
                "vision_difficulty": "none",
                "additional_needs": ["low_literacy"],
            },
            headers=headers,
        ).json()

        recommendation = result["recommendation"]
        assert recommendation["interface_mode"] == "easy"
        assert recommendation["font_size"] in ("large", "extra_large")
        assert recommendation["audio_guidance"] is True
        assert recommendation["language"] == "hi"
        assert any(r["hi"] for r in recommendation["reasons"])

        # The patient overrides it — and that must stick.
        customised = client.put(
            f"{api}/accessibility/preferences",
            json={"interface_mode": "standard", "accepted_recommendation": False},
            headers=headers,
        ).json()
        assert customised["interface_mode"] == "standard"
        assert customised["source"] == "customized"
