"""ABHA linking: mock verification and its failure paths.

The recurring theme: nothing about ABHA may block onboarding.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.modules.abha.mock_registry import REJECTED_SENTINEL, UNAVAILABLE_SENTINEL


class TestLinking:
    def test_links_a_valid_abha_number(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310001")
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": "12-3456-7890-1234"},
            headers=headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert body["abha"]["verification_status"] == "verified"
        assert body["abha"]["abha_id"] == "12-3456-7890-1234"
        assert body["abha"]["linked_at"] is not None
        assert body["abha"]["is_mock"] is True
        assert body["next_route"] == "/onboarding/personal"

    def test_accepts_an_abha_address(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310002")
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": "Rajesh.Kumar@abdm"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["abha"]["abha_id"] == "rajesh.kumar@abdm"

    def test_accepts_digits_without_separators(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310003")
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": "12345678901234"},
            headers=headers,
        )
        assert response.status_code == 200
        # Presented back in the familiar grouped form.
        assert response.json()["abha"]["abha_id"] == "12-3456-7890-1234"


class TestFailurePaths:
    def test_a_malformed_id_is_rejected_but_kept(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310010")
        response = client.post(
            f"{api}/patients/me/abha/link", json={"abha_id": "not-an-id"}, headers=headers
        )
        assert response.status_code == 422
        assert "14-digit" in response.json()["error"]["message"]

        # The attempt is recorded and the entered value preserved.
        state = client.get(f"{api}/patients/me/abha", headers=headers).json()
        assert state["verification_status"] == "failed"
        assert state["abha_id"] == "not-an-id"
        assert state["failure_reason"]

    def test_a_rejected_id_records_the_reason(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310011")
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": REJECTED_SENTINEL},
            headers=headers,
        )
        assert response.status_code == 422
        state = client.get(f"{api}/patients/me/abha", headers=headers).json()
        assert state["verification_status"] == "failed"

    def test_registry_unavailable_degrades_gracefully(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812310012")
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": UNAVAILABLE_SENTINEL},
            headers=headers,
        )
        assert response.status_code == 503
        assert "continue" in response.json()["error"]["message"].lower()

        # Input preserved, status not falsely marked failed, and the patient
        # can still move on.
        state = client.get(f"{api}/patients/me/abha", headers=headers).json()
        assert state["abha_id"] == UNAVAILABLE_SENTINEL
        assert state["verification_status"] == "unverified"

        skipped = client.post(f"{api}/patients/me/abha/skip", headers=headers)
        assert skipped.status_code == 200
        assert skipped.json()["next_route"] == "/onboarding/personal"

    def test_a_failed_attempt_does_not_block_onboarding(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812310013")
        client.post(
            f"{api}/patients/me/abha/link", json={"abha_id": "rubbish"}, headers=headers
        )
        response = client.post(f"{api}/patients/me/abha/skip", headers=headers)
        assert response.status_code == 200
        assert response.json()["onboarding_status"] == "personal_info_pending"

    def test_retry_after_failure_succeeds(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310014")
        client.post(
            f"{api}/patients/me/abha/link", json={"abha_id": "oops"}, headers=headers
        )
        response = client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": "11-2233-4455-6677"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["abha"]["verification_status"] == "verified"
        assert response.json()["abha"]["failure_reason"] is None


class TestSkip:
    def test_skipping_advances_onboarding(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812310020")
        response = client.post(f"{api}/patients/me/abha/skip", headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body["abha"]["verification_status"] == "skipped"
        assert body["notice"]

    def test_skipping_does_not_undo_a_verified_link(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812310021")
        client.post(
            f"{api}/patients/me/abha/link",
            json={"abha_id": "12-3456-7890-9999"},
            headers=headers,
        )
        response = client.post(f"{api}/patients/me/abha/skip", headers=headers)
        assert response.json()["abha"]["verification_status"] == "verified"
