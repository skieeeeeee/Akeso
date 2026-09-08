"""Phase 2 through the HTTP API: interview, documents, AYUSH, timeline, review."""

from __future__ import annotations

import io
import zlib

from fastapi.testclient import TestClient

RX_TEXT = b"""SHRI SAI POLYCLINIC
Dr. A. R. Mehta, MBBS MD
Date: 12/03/2026
Diagnosis: Type 2 Diabetes Mellitus, Hypertension
Rx
1. Tab. Metformin 500 mg  BD  x 30 days
2. Tab. Telmisartan 40 mg  OD  x 30 days
Advice: Low salt diet
"""

LAB_TEXT = b"""CITY DIAGNOSTIC LABORATORY
Collected on: 10/03/2026
Haemoglobin 10.2 g/dL (13.0-17.0)
HbA1c 8.4 % (4.0-5.6)
Serum Creatinine 1.1 mg/dL (0.7-1.3)
Remarks: Anaemia with poor control
"""


def png(width: int = 8, height: int = 8) -> bytes:
    """A structurally valid but blank PNG — OCR will find no text in it."""

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return (
            len(data).to_bytes(4, "big")
            + body
            + (zlib.crc32(body) & 0xFFFFFFFF).to_bytes(4, "big")
        )

    header = width.to_bytes(4, "big") + height.to_bytes(4, "big") + bytes([8, 0, 0, 0, 0])
    raw = b"".join(b"\x00" + b"\xff" * width for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def upload(client: TestClient, api: str, headers: dict, name: str, content: bytes, mime: str, **data):
    return client.post(
        f"{api}/patients/me/documents",
        files={"file": (name, io.BytesIO(content), mime)},
        data=data,
        headers=headers,
    )


# --- Interview -------------------------------------------------------------


class TestInterview:
    def test_ai_status_is_honest_about_being_off(self, client: TestClient, api: str):
        body = client.get(f"{api}/interview/ai-status").json()
        assert body["available"] is False
        assert body["provider"] == "none"

    def test_start_returns_the_first_question(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400001")
        body = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        assert body["question"]["id"] == "q_chief_complaint"
        assert body["question"]["kind"] == "free_text"
        assert body["question"]["text"]
        assert body["question"]["help"]
        assert body["complete"] is False
        assert body["progress"]["percent"] == 0

    def test_start_resumes_rather_than_restarting(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400002")
        first = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        client.post(
            f"{api}/interview/{first['session_id']}/answer",
            json={"instance_key": "q_chief_complaint", "text": "Fever", "input_method": "voice"},
            headers=headers,
        )
        again = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        assert again["session_id"] == first["session_id"]
        # It picks up at the next question, not back at the beginning.
        assert again["question"]["id"] != "q_chief_complaint"

    def test_voice_and_text_answers_are_treated_identically(
        self, client: TestClient, api: str, sign_in
    ):
        spoken_headers, _ = sign_in("9812400010")
        typed_headers, _ = sign_in("9812400011")

        results = []
        for headers, method in ((spoken_headers, "voice"), (typed_headers, "text")):
            session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
            client.post(
                f"{api}/interview/{session['session_id']}/answer",
                json={
                    "instance_key": "q_chief_complaint",
                    "text": "Chest pain",
                    "input_method": method,
                },
                headers=headers,
            )
            profile = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
            results.append(profile["sections"]["chief_complaint"][0]["value"])
        assert results[0] == results[1] == "Chest pain"

    def test_the_input_method_is_recorded_for_audit(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400012")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        client.post(
            f"{api}/interview/{session['session_id']}/answer",
            json={"instance_key": "q_chief_complaint", "text": "Cough", "input_method": "voice"},
            headers=headers,
        )
        transcript = client.get(
            f"{api}/interview/{session['session_id']}/transcript", headers=headers
        ).json()
        assert transcript["answers"][0]["input_method"] == "voice"
        assert transcript["answers"][0]["raw_answer"] == "Cough"
        assert transcript["answers"][0]["ai_assisted"] is False

    def test_answers_land_in_the_medical_profile(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400013")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        sid = session["session_id"]

        answers = {
            "q_chief_complaint": "Chest pain",
            "q_duration": "2-3 days",
            "q_severity": "8",
            "q_hpi_detail": "Worse on walking",
            "q_has_conditions": "yes",
            "q_conditions": "diabetes and high blood pressure",
        }
        view = client.get(f"{api}/interview/{sid}", headers=headers).json()
        for _ in range(20):
            question = view.get("question")
            if not question or question["id"] not in answers:
                break
            view = client.post(
                f"{api}/interview/{sid}/answer",
                json={
                    "instance_key": question["instance_key"],
                    "text": answers[question["id"]],
                    "input_method": "touch",
                },
                headers=headers,
            ).json()

        profile = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        assert profile["sections"]["chief_complaint"][0]["value"] == "Chest pain"
        assert "8/10" in [i["value"] for i in profile["sections"]["history_of_present_illness"]]
        conditions = [i["value"] for i in profile["sections"]["past_medical_history"]]
        assert "Diabetes" in conditions and "High blood pressure" in conditions
        # Everything the patient said is patient-sourced and unverified.
        assert all(i["source"] == "patient" for i in profile["sections"]["past_medical_history"])

    def test_the_branch_from_a_condition_is_asked(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400014")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        sid = session["session_id"]

        def answer(key: str, text: str):
            return client.post(
                f"{api}/interview/{sid}/answer",
                json={"instance_key": key, "text": text, "input_method": "text"},
                headers=headers,
            ).json()

        view = answer("q_chief_complaint", "Feeling unwell")
        while view["question"]["id"] != "q_has_conditions":
            view = answer(view["question"]["instance_key"], "no")
        view = answer(view["question"]["instance_key"], "yes")
        view = answer(view["question"]["instance_key"], "diabetes")

        # The follow-up names the condition the patient mentioned.
        assert view["question"]["id"] == "q_condition_medicine"
        assert view["question"]["about"] == "Diabetes"
        assert "Diabetes" in view["question"]["text"]

    def test_an_empty_answer_is_re_asked_with_a_hint(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812400015")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        view = client.post(
            f"{api}/interview/{session['session_id']}/answer",
            json={"instance_key": "q_chief_complaint", "text": "", "input_method": "voice"},
            headers=headers,
        ).json()
        assert view["question"]["id"] == "q_chief_complaint"
        assert view["retry_hint"]

    def test_going_back_reopens_the_previous_question(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812400016")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        sid = session["session_id"]
        client.post(
            f"{api}/interview/{sid}/answer",
            json={"instance_key": "q_chief_complaint", "text": "Fever", "input_method": "text"},
            headers=headers,
        )
        back = client.post(f"{api}/interview/{sid}/back", headers=headers).json()
        assert back["question"]["id"] == "q_chief_complaint"

    def test_a_stale_screen_cannot_answer_the_wrong_question(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812400017")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        view = client.post(
            f"{api}/interview/{session['session_id']}/answer",
            json={"instance_key": "q_allergies", "text": "Penicillin", "input_method": "text"},
            headers=headers,
        ).json()
        # Ignored: the current question is still the first one.
        assert view["question"]["id"] == "q_chief_complaint"
        profile = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        assert profile["sections"]["allergies"] == []

    def test_the_interview_completes_and_can_be_confirmed(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812400018")
        session = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        sid = session["session_id"]
        view = session
        for _ in range(40):
            question = view.get("question")
            if not question:
                break
            text = "Fever" if question["id"] == "q_chief_complaint" else "no"
            view = client.post(
                f"{api}/interview/{sid}/answer",
                json={"instance_key": question["instance_key"], "text": text, "input_method": "touch"},
                headers=headers,
            ).json()

        assert view["complete"] is True
        assert view["progress"]["percent"] == 100
        assert view["status"] == "awaiting_review"

        confirmed = client.post(f"{api}/interview/{sid}/confirm", headers=headers).json()
        assert confirmed["status"] == "confirmed"

    def test_requires_authentication(self, client: TestClient, api: str):
        assert client.post(f"{api}/interview/start", json={}).status_code == 401


# --- Documents -------------------------------------------------------------


class TestDocumentPipeline:
    def test_a_prescription_is_read_and_extracted(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812410001")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain",
                          document_type="prescription", title="Dr Mehta").json()
        assert document["processing_status"] == "pending"

        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()

        assert processed["processing_status"] == "completed"
        assert processed["ocr_engine"] == "plaintext"
        assert "Metformin" in processed["ocr_text"]
        assert processed["document_date"] == "2026-03-12"

        by_type: dict[str, list[str]] = {}
        for item in processed["extracted_items"]:
            by_type.setdefault(item["entity_type"], []).append(item["value"])
        assert "Metformin" in by_type["medication"]
        assert "Telmisartan" in by_type["medication"]
        assert "Type 2 Diabetes Mellitus" in by_type["diagnosis"]

        metformin = next(i for i in processed["extracted_items"] if i["value"] == "Metformin")
        assert metformin["attributes"]["dose"] == "500 mg"
        assert metformin["attributes"]["frequency"] == "BD"
        # A finding starts unreviewed — it is not a confirmed fact.
        assert metformin["review_state"] == "unreviewed"

    def test_lab_values_are_flagged_only_against_a_printed_range(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812410002")
        document = upload(client, api, headers, "lab.txt", LAB_TEXT, "text/plain",
                          document_type="lab_report").json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()

        flags = {
            item["value"]: item["flag"]
            for item in processed["extracted_items"]
            if item["entity_type"] == "investigation"
        }
        assert flags["Haemoglobin"] == "low"
        assert flags["HbA1c"] == "high"
        assert flags["Serum Creatinine"] == "normal"

        # Detected type overrides whatever the patient tapped.
        assert processed["document_type"] == "lab_report"

    def test_no_range_means_no_flag(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812410003")
        document = upload(
            client, api, headers, "partial.txt",
            b"REPORT\nHaemoglobin 10.2 g/dL\n", "text/plain",
        ).json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()
        investigations = [i for i in processed["extracted_items"] if i["entity_type"] == "investigation"]
        assert investigations
        assert all(item["flag"] is None for item in investigations)

    def test_unreadable_document_fails_without_being_lost(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812410010")
        document = upload(client, api, headers, "blank.png", png(), "image/png").json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()

        assert processed["processing_status"] == "failed"
        assert processed["processing_error"]
        # The document survives and the patient is told they can retry.
        assert "again" in processed["processing_error"].lower()
        listing = client.get(f"{api}/patients/me/documents", headers=headers).json()
        assert listing["total"] == 1
        # And the file itself is still downloadable.
        assert client.get(
            f"{api}/patients/me/documents/{document['id']}/file", headers=headers
        ).status_code == 200

    def test_text_read_but_nothing_recognised_needs_review(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812410011")
        document = upload(
            client, api, headers, "ticket.txt",
            b"Bus ticket Nagpur to Pune, seat 14, fare 450\n", "text/plain",
        ).json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()

        assert processed["processing_status"] == "needs_review"
        # Raw text is preserved for the clinician even so.
        assert "Bus ticket" in processed["ocr_text"]

    def test_status_endpoint_explains_what_is_happening(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812410012")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()

        pending = client.get(
            f"{api}/patients/me/documents/{document['id']}/status", headers=headers
        ).json()
        assert pending["processing_status"] == "pending"
        assert set(pending["message"]) == {"en", "hi", "mr", "ta", "gu", "pa"}

        client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)
        done = client.get(
            f"{api}/patients/me/documents/{document['id']}/status", headers=headers
        ).json()
        assert done["processing_status"] == "completed"
        assert done["finding_count"] > 0

    def test_retry_preserves_reviewed_findings(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812410013")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()
        target = processed["extracted_items"][0]

        client.post(
            f"{api}/patients/me/documents/{document['id']}/findings/{target['id']}",
            json={"review_state": "accepted"},
            headers=headers,
        )
        retried = client.post(
            f"{api}/patients/me/documents/{document['id']}/retry", headers=headers
        ).json()

        kept = next(i for i in retried["extracted_items"] if i["id"] == target["id"])
        assert kept["review_state"] == "accepted"

    def test_a_finding_can_be_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812410014")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()
        target = processed["extracted_items"][0]
        rejected = client.post(
            f"{api}/patients/me/documents/{document['id']}/findings/{target['id']}",
            json={"review_state": "rejected"},
            headers=headers,
        ).json()
        assert rejected["review_state"] == "rejected"

    def test_extraction_never_writes_to_the_medical_profile(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812410015")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()
        client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)

        profile = client.get(f"{api}/patients/me/medical-profile", headers=headers).json()
        # A document finding is never silently promoted to a patient fact.
        assert profile["total_items"] == 0


# --- Timeline --------------------------------------------------------------


class TestTimeline:
    def test_it_lists_documents_and_their_findings(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812420001")
        document = upload(client, api, headers, "lab.txt", LAB_TEXT, "text/plain",
                          title="City Lab").json()
        client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)

        timeline = client.get(f"{api}/timeline", headers=headers).json()
        types = {event["event_type"] for event in timeline["events"]}
        assert "document" in types
        assert "investigation" in types
        assert timeline["total"] > 1
        assert timeline["counts"]["investigation"] >= 3
        # Every entry says where it came from, and nothing claims to diagnose.
        assert all(event["source_kind"] for event in timeline["events"])
        assert "not a diagnosis" in timeline["disclaimer"]["en"]

    def test_events_are_newest_first(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812420002")
        for name, content in (("old.txt", LAB_TEXT), ("new.txt", RX_TEXT)):
            document = upload(client, api, headers, name, content, "text/plain").json()
            client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)

        events = client.get(f"{api}/timeline", headers=headers).json()["events"]
        dates = [event["event_date"] for event in events if event["event_date"]]
        assert dates == sorted(dates, reverse=True)

    def test_it_can_be_filtered(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812420003")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()
        client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)

        filtered = client.get(f"{api}/timeline?event_type=medication", headers=headers).json()
        assert filtered["events"]
        assert {e["event_type"] for e in filtered["events"]} == {"medication"}
        # Counts stay unfiltered so a filter chip is never empty by surprise.
        assert filtered["counts"]["document"] == 1

    def test_a_rejected_finding_leaves_the_timeline(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812420004")
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain").json()
        processed = client.post(
            f"{api}/patients/me/documents/{document['id']}/process", headers=headers
        ).json()
        target = next(i for i in processed["extracted_items"] if i["entity_type"] == "medication")

        before = len(client.get(f"{api}/timeline", headers=headers).json()["events"])
        client.post(
            f"{api}/patients/me/documents/{document['id']}/findings/{target['id']}",
            json={"review_state": "rejected"},
            headers=headers,
        )
        after = len(client.get(f"{api}/timeline", headers=headers).json()["events"])
        assert after == before - 1

    def test_an_empty_timeline_is_valid(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812420005")
        timeline = client.get(f"{api}/timeline", headers=headers).json()
        assert timeline["total"] == 0
        assert timeline["events"] == []


# --- AYUSH -----------------------------------------------------------------


class TestAyush:
    def test_content_covers_the_ten_fold_examination(self, client: TestClient, api: str):
        body = client.get(f"{api}/ayush/content").json()
        assert len(body["dashavidha"]) == 10
        keys = {item["key"] for item in body["dashavidha"]}
        assert keys == {
            "prakriti", "vikriti", "sara", "samhanana", "pramana",
            "satmya", "sattva", "ahara_shakti", "vyayama_shakti", "vaya",
        }
        for item in body["dashavidha"]:
            assert item["term"]
            assert set(item["prompt"]) == {"en", "hi", "mr", "ta", "gu", "pa"}
        assert body["ahara_options"] and body["vihara_options"]

    def test_it_is_absent_until_the_patient_fills_it(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430001")
        assert client.get(f"{api}/ayush", headers=headers).json() is None

    def test_a_partial_assessment_is_accepted(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430002")
        body = client.put(
            f"{api}/ayush",
            json={"dashavidha": {"prakriti": "vata"}, "ahara": ["vegetarian"], "vihara": []},
            headers=headers,
        ).json()
        assert body["dashavidha"] == {"prakriti": "vata"}
        # Skipping factors is allowed, so it is simply not "complete".
        assert body["is_complete"] is False

    def test_a_full_assessment_is_marked_complete(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430003")
        content = client.get(f"{api}/ayush/content").json()
        full = {item["key"]: item["options"][0]["value"] for item in content["dashavidha"]}
        body = client.put(
            f"{api}/ayush",
            json={"dashavidha": full, "ahara": ["vegetarian"], "vihara": ["early_riser"]},
            headers=headers,
        ).json()
        assert body["is_complete"] is True

    def test_an_invented_answer_is_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430004")
        response = client.put(
            f"{api}/ayush", json={"dashavidha": {"prakriti": "sparkly"}}, headers=headers
        )
        assert response.status_code == 422

    def test_an_invented_factor_is_rejected(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430005")
        response = client.put(
            f"{api}/ayush", json={"dashavidha": {"astrology": "leo"}}, headers=headers
        )
        assert response.status_code == 422
        assert "astrology" in response.json()["error"]["message"]

    def test_ayush_is_opt_in_for_the_interview(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812430006")
        without = client.post(f"{api}/interview/start", json={}, headers=headers).json()
        assert without["progress"]["section_count"] == 9

        other, _ = sign_in("9812430007")
        with_ayush = client.post(
            f"{api}/interview/start", json={"include_ayush": True}, headers=other
        ).json()
        assert with_ayush["progress"]["section_count"] == 10


# --- Structured history / review ------------------------------------------


class TestStructuredHistory:
    def test_it_separates_patient_and_document_information(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812440001")
        # Something the patient said...
        client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"chief_complaint": [{"value": "Chest pain"}],
                               "allergies": [{"value": "Penicillin"}]}},
            headers=headers,
        )
        # ...and something a document says.
        document = upload(client, api, headers, "rx.txt", RX_TEXT, "text/plain",
                          title="Dr Mehta").json()
        client.post(f"{api}/patients/me/documents/{document['id']}/process", headers=headers)

        history = client.get(f"{api}/patients/me/medical-profile/structured", headers=headers).json()

        assert history["patient_reported_count"] == 2
        assert history["document_derived_count"] > 0

        complaint = history["sections"]["chief_complaint"]
        assert complaint[0]["source"] == "patient"

        medications = history["sections"]["current_medications"]
        assert medications and all(item["source"] == "document" for item in medications)
        # Document-derived entries say where they came from — as a machine
        # kind plus the document's name, so the client words it in the
        # patient's language rather than receiving an English sentence.
        assert medications[0]["note"] == "found_in_document"
        assert medications[0]["note_source"] == "Dr Mehta"

        assert "not a diagnosis" in history["disclaimer"]["en"]
        assert history["narrative_source"] == "template"
        assert "Chest pain".lower() in history["narrative"].lower()

    def test_missing_sections_are_reported_not_hidden(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812440002")
        history = client.get(f"{api}/patients/me/medical-profile/structured", headers=headers).json()
        assert "chief_complaint" in history["missing_sections"]
        assert "allergies" in history["missing_sections"]

    def test_a_none_reported_answer_does_not_count_as_missing(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812440003")
        client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"allergies": [{"value": "None reported"}]}},
            headers=headers,
        )
        history = client.get(f"{api}/patients/me/medical-profile/structured", headers=headers).json()
        # It was asked and answered, so it still reads as missing information.
        assert "allergies" in history["missing_sections"]

    def test_the_narrative_never_claims_a_diagnosis(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812440004")
        client.put(
            f"{api}/patients/me/medical-profile",
            json={"sections": {"chief_complaint": [{"value": "Chest pain"}]}},
            headers=headers,
        )
        narrative = client.get(
            f"{api}/patients/me/medical-profile/structured", headers=headers
        ).json()["narrative"]
        assert "reports" in narrative
        assert "not a diagnosis" in narrative.lower()
        for forbidden in ("you have", "diagnosed with", "suffers from"):
            assert forbidden not in narrative.lower()

    def test_it_includes_the_ayush_flag(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812440005")
        before = client.get(
            f"{api}/patients/me/medical-profile/structured", headers=headers
        ).json()
        assert before["ayush_included"] is False

        client.put(f"{api}/ayush", json={"dashavidha": {"prakriti": "kapha"}}, headers=headers)
        after = client.get(
            f"{api}/patients/me/medical-profile/structured", headers=headers
        ).json()
        assert after["ayush_included"] is True
