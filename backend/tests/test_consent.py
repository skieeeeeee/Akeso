"""Consent: granular decisions, gating, and revocation."""

from __future__ import annotations

from fastapi.testclient import TestClient

GRANT_ALL = {
    "decisions": [
        {"purpose": "health_data_collection", "granted": True},
        {"purpose": "share_with_treating_doctor", "granted": True},
        {"purpose": "abha_linkage", "granted": True},
    ]
}
GRANT_REQUIRED_ONLY = {
    "decisions": [
        {"purpose": "health_data_collection", "granted": True},
        {"purpose": "share_with_treating_doctor", "granted": True},
        {"purpose": "abha_linkage", "granted": False},
    ]
}


class TestContent:
    def test_consent_text_is_versioned_and_localised(self, client: TestClient, api: str):
        response = client.get(f"{api}/consents/content")
        assert response.status_code == 200
        body = response.json()
        assert body["version"]
        assert set(body["summary"]["title"]) == {"en", "hi", "mr", "ta", "gu", "pa"}
        assert len(body["items"]) == 3
        for item in body["items"]:
            # Each purpose must explain what, why and how.
            for key in ("what", "why", "how", "title"):
                assert set(item[key]) == {"en", "hi", "mr", "ta", "gu", "pa"}, item["purpose"]

    def test_optional_purposes_are_marked(self, client: TestClient, api: str):
        items = client.get(f"{api}/consents/content").json()["items"]
        optional = [item["purpose"] for item in items if not item["required"]]
        assert optional == ["abha_linkage"]


class TestSubmitting:
    def test_granting_everything_advances_onboarding(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330001")
        response = client.post(f"{api}/consents", json=GRANT_ALL, headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body["has_required_consents"] is True
        assert len(body["consents"]) == 3
        assert all(c["is_active"] for c in body["consents"])
        assert body["next_route"] == "/onboarding/medical-profile"

    def test_declining_an_optional_purpose_still_advances(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330002")
        body = client.post(f"{api}/consents", json=GRANT_REQUIRED_ONLY, headers=headers).json()
        assert body["has_required_consents"] is True
        declined = [c for c in body["consents"] if c["purpose"] == "abha_linkage"][0]
        assert declined["status"] == "declined"
        assert declined["declined_at"] is not None

    def test_declining_a_required_purpose_blocks_progress(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330003")
        body = client.post(
            f"{api}/consents",
            json={"decisions": [{"purpose": "health_data_collection", "granted": False}]},
            headers=headers,
        ).json()
        assert body["has_required_consents"] is False
        assert body["onboarding_status"] == "abha_pending"

    def test_the_agreed_text_version_is_recorded(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812330004")
        version = client.get(f"{api}/consents/content").json()["version"]
        body = client.post(f"{api}/consents", json=GRANT_ALL, headers=headers).json()
        assert all(c["text_version"] == version for c in body["consents"])

    def test_the_language_shown_is_recorded(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812330005")
        body = client.post(
            f"{api}/consents", json={**GRANT_ALL, "language": "hi"}, headers=headers
        ).json()
        assert all(c["language"] == "hi" for c in body["consents"])

    def test_changing_a_decision_supersedes_the_old_one(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330006")
        client.post(f"{api}/consents", json=GRANT_REQUIRED_ONLY, headers=headers)
        body = client.post(
            f"{api}/consents",
            json={"decisions": [{"purpose": "abha_linkage", "granted": True}]},
            headers=headers,
        ).json()
        abha = [c for c in body["consents"] if c["purpose"] == "abha_linkage"][0]
        assert abha["status"] == "granted"
        # One current record per purpose, not a growing pile.
        assert len(body["consents"]) == 3

    def test_resubmitting_the_same_decision_is_idempotent(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330007")
        first = client.post(f"{api}/consents", json=GRANT_ALL, headers=headers).json()
        second = client.post(f"{api}/consents", json=GRANT_ALL, headers=headers).json()
        assert len(first["consents"]) == len(second["consents"]) == 3

    def test_requires_authentication(self, client: TestClient, api: str):
        assert client.post(f"{api}/consents", json=GRANT_ALL).status_code == 401

    def test_an_unknown_purpose_is_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812330008")
        response = client.post(
            f"{api}/consents",
            json={"decisions": [{"purpose": "sell_my_data", "granted": True}]},
            headers=headers,
        )
        assert response.status_code == 422


class TestRevocation:
    def test_a_granted_consent_can_be_withdrawn(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812330020")
        client.post(f"{api}/consents", json=GRANT_ALL, headers=headers)
        body = client.post(
            f"{api}/consents/revoke", json={"purpose": "abha_linkage"}, headers=headers
        ).json()
        revoked = [c for c in body["consents"] if c["purpose"] == "abha_linkage"][0]
        assert revoked["status"] == "revoked"
        assert revoked["revoked_at"] is not None
        assert revoked["is_active"] is False

    def test_revoking_a_required_consent_removes_the_required_flag(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330021")
        client.post(f"{api}/consents", json=GRANT_ALL, headers=headers)
        body = client.post(
            f"{api}/consents/revoke",
            json={"purpose": "health_data_collection"},
            headers=headers,
        ).json()
        assert body["has_required_consents"] is False

    def test_revoking_something_never_granted_fails_clearly(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812330022")
        response = client.post(
            f"{api}/consents/revoke", json={"purpose": "abha_linkage"}, headers=headers
        )
        assert response.status_code == 404
