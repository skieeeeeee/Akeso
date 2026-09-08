"""The returning-patient journey and encounter safety, through the API.

The property under test throughout: a returning patient is asked about today
only, and their historical record is never rewritten by a visit.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

RX_TEXT = b"""Dr Mehta Clinic
Date: 12/03/2026
Diagnosis: Type 2 Diabetes Mellitus
Rx
1. Tab. Metformin 500 mg  BD  x 30 days
"""


def seed_returning(db, key: str = "standard"):
    """Create a seeded demo patient with visits and processed documents."""
    from app.cli import _seed_documents, _seed_patient, _seed_visits
    from app.modules.patient.demo import DEMO_PATIENTS

    definition = DEMO_PATIENTS[key]
    patient = _seed_patient(db, definition)
    _seed_visits(db, patient, definition)
    _seed_documents(db, patient, definition)
    db.commit()
    return patient, definition


def sign_in_demo(client: TestClient, api: str, key: str) -> dict:
    session = client.post(f"{api}/auth/demo-login", json={"demo_key": key}).json()
    return {"Authorization": f"Bearer {session['access_token']}"}


def answer_until(client, api, headers, encounter_id, answers, limit=30):
    """Answer the visit interview, returning the final view."""
    view = client.get(f"{api}/encounters/{encounter_id}", headers=headers).json()
    for _ in range(limit):
        question = view.get("question")
        if not question:
            return view
        view = client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={
                "instance_key": question["instance_key"],
                "text": answers.get(question["id"], "no"),
                "input_method": "touch",
            },
            headers=headers,
        ).json()
    raise AssertionError("visit interview did not terminate")


def start_visit(client, api, headers, system: str = "allopathy") -> dict:
    """Start a visit and answer the opening care-system question."""
    started = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
    return client.post(
        f"{api}/encounters/{started['encounter_id']}/answer",
        json={"instance_key": "e_care_system", "text": system, "input_method": "touch"},
        headers=headers,
    ).json()


ORDINARY = {
    "e_care_system": "allopathy",
    "e_complaint": "Stomach pain since yesterday",
    "e_onset": "Yesterday",
    "e_severity": "5",
    "e_describe": "Cramping around the navel",
    "e_associated": "Vomiting",
    "e_tried": "Antacid at home",
    "e_meds_changed": "no",
    "e_new_conditions": "no",
    "e_anything_else": "no",
}


class TestRecognition:
    def test_a_returning_patient_is_routed_to_their_home(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        session = client.post(f"{api}/auth/demo-login", json={"demo_key": "standard"}).json()
        assert session["is_new_patient"] is False
        assert session["onboarding"]["is_complete"] is True
        assert session["onboarding"]["next_route"] == "/profile"

    def test_home_is_populated_not_empty(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        home = client.get(f"{api}/patients/me/home", headers=headers).json()

        assert home["greeting"]["en"] == "Welcome back"
        assert home["profile_complete"] is True
        assert home["history_item_count"] > 0
        # The high-value summaries a patient would want to see.
        assert home["conditions"] and home["medications"] and home["allergies"]
        assert home["visit_count"] == 2
        assert home["last_visit"]["complaint"]
        assert home["document_count"] == 2
        assert home["recent_events"]
        assert home["visit_in_progress"] is None

    def test_a_half_onboarded_patient_is_not_shown_a_full_home(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db, "incomplete")
        headers = sign_in_demo(client, api, "incomplete")
        home = client.get(f"{api}/patients/me/home", headers=headers).json()

        assert home["profile_complete"] is False
        assert home["onboarding"]["is_complete"] is False
        # It still tells them exactly where to go.
        assert home["onboarding"]["next_route"] == "/onboarding/assessment"
        assert home["visit_count"] == 0


class TestVisitAsksOnlyAboutToday:
    def test_history_is_offered_as_context_not_as_questions(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        opening = client.post(f"{api}/encounters/start", json={}, headers=headers).json()

        # What we already know is handed over read-only...
        assert opening["existing"]["conditions"]
        assert opening["existing"]["medications"]
        assert opening["existing"]["allergies"]
        assert opening["existing"]["last_visit_complaint"]
        # ...the visit opens by asking which system of medicine this is for...
        assert opening["question"]["id"] == "e_care_system"
        assert opening["visit_type"] == "follow_up"

        # ...and only then asks about today.
        view = client.post(
            f"{api}/encounters/{opening['encounter_id']}/answer",
            json={"instance_key": "e_care_system", "text": "allopathy", "input_method": "touch"},
            headers=headers,
        ).json()
        assert view["question"]["id"] == "e_complaint"

    def test_no_question_re_asks_the_full_history(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        started = start_visit(client, api, headers)
        encounter_id = started["encounter_id"]

        asked: list[str] = []
        view = started
        for _ in range(30):
            question = view.get("question")
            if not question:
                break
            asked.append(question["id"])
            view = client.post(
                f"{api}/encounters/{encounter_id}/answer",
                json={
                    "instance_key": question["instance_key"],
                    "text": ORDINARY.get(question["id"], "no"),
                    "input_method": "text",
                },
                headers=headers,
            ).json()

        # Nothing from the profile script appears in an encounter.
        assert all(question_id.startswith("e_") for question_id in asked)
        text = " ".join(asked)
        for repeated in ("allergies", "family", "surgical", "personal", "occupation"):
            assert repeated not in text

    def test_a_visit_never_rewrites_the_historical_profile(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        before = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()

        started = start_visit(client, api, headers)
        answer_until(
            client, api, headers, started["encounter_id"],
            {**ORDINARY, "e_meds_changed": "yes", "e_meds_new": "Pantoprazole 40 mg"},
        )

        after = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        # The profile is byte-for-byte untouched: today's answers live on the
        # encounter, so history cannot be silently overwritten.
        assert after["sections"] == before["sections"]
        assert after["total_items"] == before["total_items"]

        review = client.get(
            f"{api}/encounters/{started['encounter_id']}/review", headers=headers
        ).json()
        today_meds = [entry["value"] for entry in review["today"].get("current_medications", [])]
        assert "Pantoprazole 40 mg" in today_meds

    def test_starting_twice_resumes_instead_of_duplicating(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        first = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
        second = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
        assert first["encounter_id"] == second["encounter_id"]

    def test_the_opening_complaint_can_be_supplied_at_start(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        view = client.post(
            f"{api}/encounters/start",
            json={"chief_complaint": "Headache for two days", "input_method": "voice"},
            headers=headers,
        ).json()
        assert view["chief_complaint"] == "Headache for two days"

    def test_going_back_reopens_the_previous_question(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        view = start_visit(client, api, headers)
        encounter_id = view["encounter_id"]
        client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": "e_complaint", "text": "Fever", "input_method": "text"},
            headers=headers,
        )
        back = client.post(f"{api}/encounters/{encounter_id}/back", headers=headers).json()
        assert back["question"]["id"] == "e_complaint"


class TestRedFlagWorkflow:
    def _start_urgent(self, client, api, headers):
        started = start_visit(client, api, headers)
        encounter_id = started["encounter_id"]
        view = client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={
                "instance_key": "e_complaint",
                "text": "I have crushing chest pain going into my left arm",
                "input_method": "voice",
            },
            headers=headers,
        ).json()
        return encounter_id, view

    def test_an_urgent_description_raises_the_flag_immediately(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, view = self._start_urgent(client, api, headers)

        assert view["priority"] == "urgent"
        assert view["safety"]["status"] == "active"
        assert view["safety"]["flags"]
        assert view["safety"]["flags"][0]["category"] == "chest"
        # The patient's own words, not the criterion.
        assert "crushing chest pain" in view["safety"]["flags"][0]["evidence"]
        assert view["safety"]["can_be_cleared_by_patient"] is False

    def test_the_notice_is_hedged_and_translated(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        _, view = self._start_urgent(client, api, headers)

        notice = view["safety"]["notice"]
        assert set(notice["body"]) == {"en", "hi", "mr", "ta", "gu", "pa"}
        assert "may require urgent medical attention" in notice["body"]["en"]
        assert "does not confirm" in notice["disclaimer"]["en"]
        assert notice["action_staff"]["en"] and notice["action_continue"]["en"]

    def test_progress_is_saved_before_the_emergency_screen(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)

        # The answer that triggered the flag is already recorded.
        review = client.get(f"{api}/encounters/{encounter_id}/review", headers=headers).json()
        assert review["chief_complaint"]
        assert review["today_answers"]

    def test_continuing_keeps_the_flag_and_the_priority(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)

        acknowledged = client.post(
            f"{api}/encounters/{encounter_id}/safety/acknowledge", headers=headers
        ).json()
        assert acknowledged["safety"]["acknowledged"] is True
        # Acknowledging is not an escape route.
        assert acknowledged["priority"] == "urgent"
        assert acknowledged["safety"]["status"] == "active"
        assert acknowledged["question"] is not None

    def test_the_flag_survives_the_whole_interview(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)
        client.post(f"{api}/encounters/{encounter_id}/safety/acknowledge", headers=headers)

        final = answer_until(client, api, headers, encounter_id, ORDINARY)
        assert final["priority"] == "urgent"
        assert final["safety"]["status"] == "active"

    def test_the_flag_survives_submission(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)
        answer_until(client, api, headers, encounter_id, ORDINARY)

        submitted = client.post(
            f"{api}/encounters/{encounter_id}/submit",
            json={
                "symptoms_correct": True,
                "reviewed_information": True,
                "understands_use": True,
            },
            headers=headers,
        ).json()
        assert submitted["priority"] == "urgent"
        # A flagged visit is queued for review rather than simply completed.
        assert submitted["status"] == "awaiting_review"
        assert "urgent" in submitted["message"]["en"].lower()

    def test_a_patient_cannot_lower_their_own_priority(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)

        # There is no endpoint for it, and guessing one gets a 404/405.
        for method, path in (
            ("POST", f"/encounters/{encounter_id}/safety/clear"),
            ("DELETE", f"/encounters/{encounter_id}/safety"),
            ("POST", f"/encounters/{encounter_id}/priority"),
        ):
            response = client.request(method, f"{api}{path}", json={}, headers=headers)
            assert response.status_code in (404, 405), path

        still = client.get(f"{api}/encounters/{encounter_id}/safety", headers=headers).json()
        assert still["status"] == "active"

    def test_requesting_assistance_is_recorded(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id, _ = self._start_urgent(client, api, headers)
        view = client.post(
            f"{api}/encounters/{encounter_id}/safety/assistance", headers=headers
        ).json()
        assert view["safety"]["status"] == "active"
        assert view["safety"]["acknowledged"] is True

    def test_an_ordinary_visit_is_never_flagged(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        started = start_visit(client, api, headers)
        final = answer_until(client, api, headers, started["encounter_id"], ORDINARY)

        assert final["safety"]["status"] == "none"
        assert final["safety"]["notice"] is None
        assert final["priority"] == "routine"


class TestReviewAndSubmission:
    def _completed(self, client, api, headers):
        started = start_visit(client, api, headers)
        answer_until(client, api, headers, started["encounter_id"], ORDINARY)
        return started["encounter_id"]

    def test_review_separates_today_from_history(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)

        review = client.get(f"{api}/encounters/{encounter_id}/review", headers=headers).json()
        assert review["chief_complaint"] == "Stomach pain since yesterday"
        assert review["today"]
        assert review["today_answers"]
        # Existing history is present but kept in its own section.
        assert review["existing"]["conditions"]
        assert review["existing"]["medications"]
        assert "not a diagnosis" in review["disclaimer"]["en"]
        assert review["narrative_source"] == "template"

    def test_the_narrative_states_no_diagnosis(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)
        narrative = client.get(
            f"{api}/encounters/{encounter_id}/review", headers=headers
        ).json()["narrative"]

        assert "not a diagnosis" in narrative.lower()
        for forbidden in ("you have", "diagnosed with", "suffers from", "is caused by"):
            assert forbidden not in narrative.lower()
        # Prior knowledge is labelled as prior knowledge.
        assert "earlier visits" in narrative or "on record" in narrative

    def test_submission_requires_all_three_confirmations(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)

        response = client.post(
            f"{api}/encounters/{encounter_id}/submit",
            json={
                "symptoms_correct": True,
                "reviewed_information": False,
                "understands_use": True,
            },
            headers=headers,
        )
        assert response.status_code == 422
        assert "confirm" in response.json()["error"]["message"].lower()

    def test_submission_records_a_timestamp(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)

        submitted = client.post(
            f"{api}/encounters/{encounter_id}/submit",
            json={
                "symptoms_correct": True,
                "reviewed_information": True,
                "understands_use": True,
            },
            headers=headers,
        ).json()
        assert submitted["submitted_at"]
        assert submitted["status"] == "completed"

    def test_resubmitting_does_not_duplicate(self, client: TestClient, api: str, db):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)
        payload = {
            "symptoms_correct": True,
            "reviewed_information": True,
            "understands_use": True,
        }

        first = client.post(
            f"{api}/encounters/{encounter_id}/submit", json=payload, headers=headers
        ).json()
        second = client.post(
            f"{api}/encounters/{encounter_id}/submit", json=payload, headers=headers
        ).json()

        # Idempotent: same encounter, same instant, no second visit created.
        # Compared as instants, not strings: the first response serialises a
        # fresh UTC datetime while the second is read back from PostgreSQL in
        # the session timezone.
        from datetime import datetime

        assert first["encounter_id"] == second["encounter_id"]
        assert datetime.fromisoformat(first["submitted_at"]) == datetime.fromisoformat(
            second["submitted_at"]
        )

        home = client.get(f"{api}/patients/me/home", headers=headers).json()
        assert home["visit_count"] == 3  # two seeded + this one

    def test_a_submitted_visit_cannot_be_answered_further(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        encounter_id = self._completed(client, api, headers)
        client.post(
            f"{api}/encounters/{encounter_id}/submit",
            json={
                "symptoms_correct": True,
                "reviewed_information": True,
                "understands_use": True,
            },
            headers=headers,
        )
        response = client.post(
            f"{api}/encounters/{encounter_id}/answer",
            json={"instance_key": "e_complaint", "text": "changed my mind", "input_method": "text"},
            headers=headers,
        )
        assert response.status_code == 409

    def test_a_visit_with_no_complaint_cannot_be_submitted(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        started = client.post(f"{api}/encounters/start", json={}, headers=headers).json()
        response = client.post(
            f"{api}/encounters/{started['encounter_id']}/submit",
            json={
                "symptoms_correct": True,
                "reviewed_information": True,
                "understands_use": True,
            },
            headers=headers,
        )
        assert response.status_code == 422

    def test_home_offers_to_resume_an_unfinished_visit(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db)
        headers = sign_in_demo(client, api, "standard")
        client.post(
            f"{api}/encounters/start",
            json={"chief_complaint": "Back pain"},
            headers=headers,
        )
        home = client.get(f"{api}/patients/me/home", headers=headers).json()
        assert home["visit_in_progress"]["complaint"] == "Back pain"


class TestAuthorisationBoundaries:
    def test_a_patient_cannot_read_another_patients_visit(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db, "standard")
        seed_returning(db, "easy")

        mine = sign_in_demo(client, api, "standard")
        started = client.post(f"{api}/encounters/start", json={}, headers=mine).json()

        theirs = sign_in_demo(client, api, "easy")
        for path in ("", "/review", "/safety"):
            response = client.get(
                f"{api}/encounters/{started['encounter_id']}{path}", headers=theirs
            )
            assert response.status_code == 404, path

    def test_a_patient_cannot_answer_another_patients_visit(
        self, client: TestClient, api: str, db
    ):
        seed_returning(db, "standard")
        seed_returning(db, "easy")
        mine = sign_in_demo(client, api, "standard")
        started = client.post(f"{api}/encounters/start", json={}, headers=mine).json()

        theirs = sign_in_demo(client, api, "easy")
        response = client.post(
            f"{api}/encounters/{started['encounter_id']}/answer",
            json={"instance_key": "e_complaint", "text": "x", "input_method": "text"},
            headers=theirs,
        )
        assert response.status_code == 404

    def test_every_encounter_route_requires_a_session(self, client: TestClient, api: str):
        assert client.post(f"{api}/encounters/start", json={}).status_code == 401
        assert client.get(f"{api}/encounters/current").status_code == 401
        assert client.get(f"{api}/patients/me/home").status_code == 401
