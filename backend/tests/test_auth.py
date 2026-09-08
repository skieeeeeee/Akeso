"""Authentication: mocked OTP, returning-patient detection, demo sign-in."""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestOtpRequest:
    def test_issues_a_prototype_code(self, client: TestClient, api: str):
        response = client.post(f"{api}/auth/otp/request", json={"mobile_number": "9812300010"})
        assert response.status_code == 200
        body = response.json()
        assert body["mobile_number"] == "9812300010"
        assert body["is_prototype_delivery"] is True
        assert body["prototype_code"] and len(body["prototype_code"]) == 6
        assert body["expires_in_seconds"] > 0

    def test_normalises_how_patients_actually_type_numbers(self, client: TestClient, api: str):
        for raw in ("+91 98123 00011", "098123-00011", "9812300011", "+919812300011"):
            response = client.post(f"{api}/auth/otp/request", json={"mobile_number": raw})
            assert response.status_code == 200, raw
            assert response.json()["mobile_number"] == "9812300011"

    def test_rejects_an_invalid_number_with_an_actionable_message(
        self, client: TestClient, api: str
    ):
        response = client.post(f"{api}/auth/otp/request", json={"mobile_number": "12345"})
        assert response.status_code == 422
        assert "10-digit" in response.json()["error"]["message"]

    def test_a_new_request_supersedes_the_previous_code(self, client: TestClient, api: str):
        first = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": "9812300012"}
        ).json()["prototype_code"]
        client.post(f"{api}/auth/otp/request", json={"mobile_number": "9812300012"})

        response = client.post(
            f"{api}/auth/otp/verify", json={"mobile_number": "9812300012", "code": first}
        )
        assert response.status_code == 401


class TestOtpVerify:
    def test_first_sign_in_creates_the_patient(self, client: TestClient, api: str):
        code = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": "9812300020"}
        ).json()["prototype_code"]
        response = client.post(
            f"{api}/auth/otp/verify",
            json={"mobile_number": "9812300020", "code": code, "language": "hi"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["is_new_patient"] is True
        assert body["patient"]["mobile_number"] == "9812300020"
        assert body["patient"]["preferred_language"] == "hi"
        # No name yet — it is collected in the personal-information step.
        assert body["patient"]["full_name"] is None
        assert body["patient"]["display_name"] == "New patient"
        assert body["onboarding"]["next_route"] == "/onboarding/abha"
        assert body["access_token"]

    def test_returning_sign_in_recognises_the_same_patient(
        self, client: TestClient, api: str, sign_in
    ):
        _, first = sign_in("9812300021")
        _, second = sign_in("9812300021")

        assert first["is_new_patient"] is True
        assert second["is_new_patient"] is False
        assert second["patient"]["id"] == first["patient"]["id"]

    def test_wrong_code_reports_remaining_attempts(self, client: TestClient, api: str):
        client.post(f"{api}/auth/otp/request", json={"mobile_number": "9812300022"})
        response = client.post(
            f"{api}/auth/otp/verify", json={"mobile_number": "9812300022", "code": "000000"}
        )
        assert response.status_code == 401
        assert "attempt" in response.json()["error"]["message"].lower()

    def test_locks_out_after_too_many_attempts(self, client: TestClient, api: str):
        from app.config import settings

        client.post(f"{api}/auth/otp/request", json={"mobile_number": "9812300023"})
        for _ in range(settings.otp_max_attempts):
            client.post(
                f"{api}/auth/otp/verify",
                json={"mobile_number": "9812300023", "code": "111111"},
            )
        response = client.post(
            f"{api}/auth/otp/verify", json={"mobile_number": "9812300023", "code": "111111"}
        )
        assert response.status_code == 401
        assert "request a new code" in response.json()["error"]["message"].lower()

    def test_verifying_without_a_request_fails_cleanly(self, client: TestClient, api: str):
        response = client.post(
            f"{api}/auth/otp/verify", json={"mobile_number": "9812300024", "code": "123456"}
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "authentication_failed"

    def test_a_code_cannot_be_reused(self, client: TestClient, api: str):
        code = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": "9812300025"}
        ).json()["prototype_code"]
        assert (
            client.post(
                f"{api}/auth/otp/verify",
                json={"mobile_number": "9812300025", "code": code},
            ).status_code
            == 200
        )
        replay = client.post(
            f"{api}/auth/otp/verify", json={"mobile_number": "9812300025", "code": code}
        )
        assert replay.status_code == 401


class TestSessionGuard:
    def test_protected_route_requires_a_token(self, client: TestClient, api: str):
        response = client.get(f"{api}/patients/me")
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "authentication_failed"

    def test_a_garbage_token_is_rejected(self, client: TestClient, api: str):
        response = client.get(
            f"{api}/patients/me", headers={"Authorization": "Bearer not-a-jwt"}
        )
        assert response.status_code == 401

    def test_me_returns_the_signed_in_patient(self, client: TestClient, api: str, sign_in):
        headers, session = sign_in("9812300030")
        response = client.get(f"{api}/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["patient"]["id"] == session["patient"]["id"]


class TestDemoSignIn:
    def test_demo_patients_are_listed(self, client: TestClient, api: str):
        response = client.get(f"{api}/auth/demo-patients")
        assert response.status_code == 200
        keys = {row["demo_key"] for row in response.json()}
        assert keys == {"standard", "easy", "low_vision", "incomplete"}

    def test_demo_login_requires_seeded_data(self, client: TestClient, api: str):
        # The database is empty in tests, so this must fail gracefully.
        response = client.post(f"{api}/auth/demo-login", json={"demo_key": "standard"})
        assert response.status_code == 404
        assert "seed" in str(response.json()["error"]["details"]).lower()

    def test_unknown_demo_key_is_rejected(self, client: TestClient, api: str):
        response = client.post(f"{api}/auth/demo-login", json={"demo_key": "nope"})
        assert response.status_code == 422

    def test_demo_login_works_once_seeded(self, client: TestClient, api: str, db):
        from app.cli import _seed_patient
        from app.modules.patient.demo import DEMO_PATIENTS

        _seed_patient(db, DEMO_PATIENTS["standard"])
        db.commit()

        response = client.post(f"{api}/auth/demo-login", json={"demo_key": "standard"})
        assert response.status_code == 200
        body = response.json()
        assert body["patient"]["full_name"] == "Rajesh Kumar"
        assert body["patient"]["is_demo"] is True
        assert body["onboarding"]["is_complete"] is True
