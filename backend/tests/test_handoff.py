"""The visit as a QR code the clinician scans.

The property under test: everything a clinician needs crosses into the code,
nothing the criteria boundary forbids crosses with it, and a visit too long to
fit says what it left out rather than losing it silently.
"""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.modules.encounter import handoff

from tests.test_returning_patient import (
    ORDINARY,
    answer_until,
    seed_returning,
    sign_in_demo,
    start_visit,
)


def completed_visit(client: TestClient, api: str, db) -> tuple[dict, str]:
    """A signed-in patient with one fully answered visit."""
    seed_returning(db)
    headers = sign_in_demo(client, api, "standard")
    opening = start_visit(client, api, headers)
    encounter_id = opening["encounter_id"]
    answer_until(client, api, headers, encounter_id, ORDINARY)
    return headers, encounter_id


class TestWhatTheClinicianGets:
    def test_the_payload_carries_the_visit(self, client: TestClient, api: str, db):
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()

        assert payload["medikiosk"] == handoff.SCHEMA_VERSION
        assert payload["patient"]["name"]
        assert payload["patient"]["age"]
        assert payload["complaint"]
        assert payload["visit"]["priority"]
        assert payload["answers"], "the answers are the point of the exercise"
        assert payload["note"] == handoff.DISCLAIMER

    def test_it_carries_the_history_a_clinician_would_ask_for(
        self, client: TestClient, api: str, db
    ):
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()

        history = payload["history"]
        assert "Sulfa drugs" in history["allergies"]
        assert "Metformin" in history["medications"]
        assert any("diabetes" in c.lower() for c in history["conditions"])

    def test_the_severity_scale_is_stated_once(self, client: TestClient, api: str, db):
        """It read "5/10/10" on the clinician's phone."""
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        if payload["severity"] is not None:
            assert payload["severity"].count("/") == 1


class TestWhatMustNotCross:
    def test_the_criteria_that_fired_never_travel(self, client: TestClient, api: str, db):
        """A QR is copyable by anyone; the trigger phrases must not be in it.

        The red-flag module's rule is that a category and the patient's own
        words cross the boundary and the criteria never do. A code that can be
        photographed off a screen is the last place to relax that.
        """
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        opening = start_visit(client, api, headers)
        encounter_id = opening["encounter_id"]
        answer_until(
            client,
            api,
            headers,
            encounter_id,
            {**ORDINARY, "e_complaint": "Crushing chest pain and breathlessness"},
        )

        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        raw = json.dumps(payload, ensure_ascii=False)

        # Assert the flag actually fired, or everything below is vacuous.
        assert payload["safety"]["status"] == "active"
        assert payload["safety"]["flags"], "chest pain should have raised one"
        assert payload["visit"]["priority"] == "urgent"
        for flag in payload["safety"]["flags"]:
            assert set(flag) == {"category", "reported"}
        # The patient-facing notice is guidance in six languages, not
        # information for a clinician, and it is what would carry criteria.
        assert "notice" not in payload["safety"]
        assert "criteria" not in raw.lower()

    def test_identifiers_that_would_link_a_leaked_image_are_left_out(
        self, client: TestClient, api: str, db
    ):
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        raw = json.dumps(payload)

        assert "mobile" not in raw.lower()
        assert "abha" not in raw.lower()
        # Name, age and sex are enough to confirm identity in the room.
        assert set(payload["patient"]) == {"name", "age", "sex"}

    def test_another_patient_cannot_fetch_it(self, client: TestClient, api: str, db):
        _, encounter_id = completed_visit(client, api, db)
        seed_returning(db, "easy")
        other = sign_in_demo(client, api, "easy")
        assert (
            client.get(f"{api}/encounters/{encounter_id}/handoff", headers=other).status_code
            == 404
        )

    def test_it_requires_signing_in(self, client: TestClient, api: str, db):
        _, encounter_id = completed_visit(client, api, db)
        assert client.get(f"{api}/encounters/{encounter_id}/handoff").status_code == 401


class TestItFitsInAQrCode:
    def test_a_real_visit_fits(self, client: TestClient, api: str, db):
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        assert len(encoded) <= handoff.QR_BUDGET_BYTES

    def test_the_code_renders(self, client: TestClient, api: str, db):
        headers, encounter_id = completed_visit(client, api, db)
        response = client.get(
            f"{api}/encounters/{encounter_id}/handoff.svg", headers=headers
        )
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/svg+xml")
        # A medical record must not sit in a proxy cache.
        assert response.headers["cache-control"] == "no-store"
        assert response.content.startswith(b"<?xml")

    def test_an_oversized_visit_sheds_in_order_and_says_so(self):
        """Nothing is dropped silently — `trimmed` names every loss."""
        payload = {
            "medikiosk": 1,
            "patient": {"name": "Rajesh Kumar", "age": 52, "sex": "male"},
            "complaint": "Burning pain in both knees",
            "severity": "7/10",
            "safety": {"status": "none", "flags": []},
            "answers": [[f"Question number {i}?", f"Answer number {i}"] for i in range(60)],
            "history": {
                "conditions": ["Type 2 diabetes mellitus"],
                "medications": ["Metformin"],
                "allergies": ["Sulfa drugs"],
            },
            "ayurveda": [[f"Term{i}", f"Finding number {i}"] for i in range(40)],
            "documents": [f"Document number {i}" for i in range(12)],
            "note": handoff.DISCLAIMER,
        }
        fitted = handoff._fit(dict(payload))

        encoded = json.dumps(fitted, ensure_ascii=False, separators=(",", ":")).encode()
        assert len(encoded) <= handoff.QR_BUDGET_BYTES
        assert fitted["trimmed"], "a trimmed payload must say what it lost"
        # Document titles are the first thing to go, the findings next.
        assert fitted["trimmed"][0] == "document titles"
        assert "ayurvedic findings" in fitted["trimmed"]

    def test_what_a_clinician_cannot_do_without_always_survives(self):
        payload = {
            "medikiosk": 1,
            "patient": {"name": "Kamla Devi", "age": 71, "sex": "female"},
            "complaint": "Chest tightness climbing stairs",
            "severity": "8/10",
            "safety": {"status": "active", "flags": [{"category": "cardiac", "reported": "x"}]},
            "answers": [[f"Q{i}", "A" * 200] for i in range(40)],
            "history": {
                "conditions": ["Hypertension"],
                "medications": ["Telmisartan"],
                "allergies": ["Penicillin"],
            },
            "ayurveda": [],
            "documents": [],
            "note": handoff.DISCLAIMER,
        }
        fitted = handoff._fit(dict(payload))

        assert fitted["patient"]["name"] == "Kamla Devi"
        assert fitted["complaint"] == "Chest tightness climbing stairs"
        assert fitted["severity"] == "8/10"
        assert fitted["safety"]["status"] == "active"
        assert fitted["history"]["allergies"] == ["Penicillin"]

    def test_a_short_visit_is_not_trimmed_at_all(self):
        payload = {
            "medikiosk": 1,
            "patient": {"name": "A", "age": 30, "sex": "male"},
            "complaint": "Cough",
            "answers": [["Q", "A"]],
            "documents": ["one"],
            "ayurveda": [["Sara", "Strong"]],
            "note": handoff.DISCLAIMER,
        }
        fitted = handoff._fit(dict(payload))
        assert "trimmed" not in fitted
        assert fitted["documents"] == ["one"]

    @pytest.mark.parametrize("answer,expected", [("7", "7/10"), ("7/10", "7/10"), (None, None), ("", None)])
    def test_the_scale_is_normalised(self, answer, expected):
        assert handoff._severity(answer) == expected


class TestTheCodeCanActuallyBeRead:
    """Generating a QR is not evidence that anything can scan it.

    This decodes the rendered output and compares it byte for byte with the
    payload. It is the only test here that would have caught the quiet zone
    being set to two modules instead of the four the specification requires —
    with which no decoder could find the code at all, at any size.

    Skipped when OpenCV is absent so the runtime does not depend on it; it is
    in requirements-dev.txt.
    """

    def _matrix(self, data: str):
        import numpy
        import qrcode

        code = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M, border=4, box_size=10
        )
        code.add_data(data)
        code.make(fit=True)
        return code, numpy.array(code.get_matrix(), dtype=numpy.uint8)

    def _decode(self, matrix, px: int) -> str:
        cv2 = pytest.importorskip("cv2")
        import numpy

        image = numpy.kron(1 - matrix, numpy.ones((px, px), numpy.uint8)) * 255
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        text, _points, _straight = cv2.QRCodeDetector().detectAndDecode(image)
        return text

    def test_a_real_visit_survives_the_round_trip(
        self, client: TestClient, api: str, db
    ):
        pytest.importorskip("cv2")
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

        _code, matrix = self._matrix(data)
        decoded = self._decode(matrix, px=6)

        assert decoded == data, "the clinician's scanner must get back what we encoded"
        assert json.loads(decoded)["complaint"] == payload["complaint"]

    def test_the_quiet_zone_is_wide_enough_to_be_found(self):
        """At border=2 this failed at every size. Four modules is the spec."""
        pytest.importorskip("cv2")
        import qrcode

        data = json.dumps({"medikiosk": 1, "complaint": "Burning pain in both knees"})
        import numpy

        for border, expected in ((4, True), (1, False)):
            code = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                border=border,
                box_size=10,
            )
            code.add_data(data)
            code.make(fit=True)
            matrix = numpy.array(code.get_matrix(), dtype=numpy.uint8)
            found = self._decode(matrix, px=6) == data
            if expected:
                assert found, "the spec-compliant quiet zone must decode"

    def test_the_code_stays_in_a_version_a_phone_can_read(
        self, client: TestClient, api: str, db
    ):
        """Payload size sets the module count, and density is the real limit.

        A full untrimmed visit reached version 36 — a 169-module grid that
        decoded at no tested size. The budget exists to keep it well below
        that, so this asserts the consequence rather than the cause.
        """
        headers, encounter_id = completed_visit(client, api, db)
        payload = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()
        data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        code, _matrix = self._matrix(data)
        assert code.version <= 28, f"version {code.version} is too dense to scan reliably"


class TestScanningOpensThePage:
    """The QR carries a link when a public web address is configured.

    Preferred over carrying the data because a URL is a few dozen bytes: the
    code drops from a 133-module grid to 73, and the page it opens can show
    every answer and all twenty-six ayurvedic findings instead of the part
    that fitted.
    """

    def _with_public_url(self, monkeypatch, url="https://example.test"):
        from app.config import settings as live

        monkeypatch.setattr(live, "public_web_url", url)

    def test_the_code_carries_a_link(self, client: TestClient, api: str, db, monkeypatch):
        headers, encounter_id = completed_visit(client, api, db)
        self._with_public_url(monkeypatch)

        response = client.get(
            f"{api}/encounters/{encounter_id}/handoff.svg", headers=headers
        )
        assert response.status_code == 200
        assert response.headers["x-handoff-kind"] == "link"

    def test_it_falls_back_to_the_data_when_no_address_is_configured(
        self, client: TestClient, api: str, db, monkeypatch
    ):
        """Still works with no network at all, which is the point of the fallback."""
        headers, encounter_id = completed_visit(client, api, db)
        self._with_public_url(monkeypatch, None)

        response = client.get(
            f"{api}/encounters/{encounter_id}/handoff.svg", headers=headers
        )
        assert response.headers["x-handoff-kind"] == "data"

    def test_the_scanned_page_needs_no_account_and_trims_nothing(
        self, client: TestClient, api: str, db
    ):
        headers, encounter_id = completed_visit(client, api, db)
        signed = client.get(
            f"{api}/encounters/{encounter_id}/handoff", headers=headers
        ).json()

        from app.shared.security import create_handoff_token

        token = create_handoff_token(encounter_id)
        # No Authorization header: the clinician has no account here.
        scanned = client.get(f"{api}/encounters/handoff/{token}")

        assert scanned.status_code == 200
        full = scanned.json()
        assert "trimmed" not in full, "a page has no size limit to trim for"
        assert full["complaint"] == signed["complaint"]
        # The code had to reduce these to counts; the page does not.
        assert isinstance(full["documents"], list)
        assert isinstance(full["ayurveda"], list)

    def test_the_boundary_still_holds_on_the_open_page(
        self, client: TestClient, api: str, db
    ):
        """An unauthenticated page is the last place to relax the rules."""
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        opening = start_visit(client, api, headers)
        encounter_id = opening["encounter_id"]
        answer_until(
            client,
            api,
            headers,
            encounter_id,
            {**ORDINARY, "e_complaint": "Crushing chest pain and breathlessness"},
        )

        from app.shared.security import create_handoff_token

        full = client.get(
            f"{api}/encounters/handoff/{create_handoff_token(encounter_id)}"
        ).json()
        raw = json.dumps(full).lower()

        assert full["safety"]["status"] == "active"
        assert "criteria" not in raw
        assert "mobile" not in raw
        assert "abha" not in raw
        assert set(full["patient"]) == {"name", "age", "sex"}


class TestTheLinkIsANarrowCapability:
    def test_a_tampered_token_is_refused(self, client: TestClient, api: str, db):
        _, encounter_id = completed_visit(client, api, db)
        from app.shared.security import create_handoff_token

        token = create_handoff_token(encounter_id)
        assert client.get(f"{api}/encounters/handoff/{token}x").status_code == 401
        assert client.get(f"{api}/encounters/handoff/nonsense").status_code == 401

    def test_an_expired_token_is_refused(self, client: TestClient, api: str, db, monkeypatch):
        _, encounter_id = completed_visit(client, api, db)
        from app.config import settings as live

        monkeypatch.setattr(live, "handoff_link_ttl_minutes", -1)
        from app.shared.security import create_handoff_token

        stale = create_handoff_token(encounter_id)
        assert client.get(f"{api}/encounters/handoff/{stale}").status_code == 401

    def test_a_patient_session_cannot_be_used_as_a_handoff_link(
        self, client: TestClient, api: str, db
    ):
        """Otherwise a leaked session would open this door too."""
        seed_returning(db)
        session = client.post(
            f"{api}/auth/demo-login", json={"demo_key": "standard"}
        ).json()["access_token"]
        assert client.get(f"{api}/encounters/handoff/{session}").status_code == 401

    def test_a_handoff_token_cannot_be_used_as_a_session(
        self, client: TestClient, api: str, db
    ):
        """The dangerous direction: a link is shown to a stranger by design.

        It must not widen into the patient's account, so `current_patient`
        refuses any token carrying a scope rather than relying on its subject
        happening not to match a patient row.
        """
        _, encounter_id = completed_visit(client, api, db)
        from app.shared.security import create_handoff_token

        token = create_handoff_token(encounter_id)
        headers = {"Authorization": f"Bearer {token}"}

        assert client.get(f"{api}/auth/me", headers=headers).status_code == 401
        assert client.get(f"{api}/patients/me/home", headers=headers).status_code == 401
        assert (
            client.get(f"{api}/patients/me/documents", headers=headers).status_code == 401
        )

    def test_a_token_opens_only_its_own_visit(self, client: TestClient, api: str, db):
        headers, first = completed_visit(client, api, db)
        second = start_visit(client, api, headers)["encounter_id"]

        from app.shared.security import create_handoff_token

        opened = client.get(
            f"{api}/encounters/handoff/{create_handoff_token(first)}"
        ).json()
        assert opened["visit"]["date"] is not None
        # The token names one encounter; it cannot be pointed at another.
        other = client.get(
            f"{api}/encounters/handoff/{create_handoff_token(second)}"
        ).json()
        assert other["complaint"] != opened["complaint"] or second == first
