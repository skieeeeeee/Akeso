"""Previous medical records: stored in Phase 1, read in Phase 2."""

from __future__ import annotations

import io
import zlib

import pytest
from fastapi.testclient import TestClient

from app.modules.documents import extraction


def png_bytes(width: int = 8, height: int = 8) -> bytes:
    """A structurally valid 1-bit-per-channel greyscale PNG."""

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


def upload(client: TestClient, api: str, headers: dict, **kwargs):
    return client.post(
        f"{api}/patients/me/documents",
        files={"file": kwargs.get("file", ("record.png", io.BytesIO(png_bytes()), "image/png"))},
        data={k: v for k, v in kwargs.items() if k != "file"},
        headers=headers,
    )


class TestUpload:
    def test_stores_a_record(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350001")
        response = upload(client, api, headers, document_type="prescription", title="Dr Mehta")
        assert response.status_code == 201
        body = response.json()
        assert body["document_type"] == "prescription"
        assert body["title"] == "Dr Mehta"
        assert body["size_bytes"] > 0
        # Phase 1 does not claim to have read the document.
        assert body["processing_status"] == "pending"
        assert body["extracted_data"] is None

    def test_accepts_a_pdf(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350002")
        response = upload(
            client,
            api,
            headers,
            file=("report.pdf", io.BytesIO(b"%PDF-1.4\n%%EOF\n"), "application/pdf"),
        )
        assert response.status_code == 201

    def test_rejects_an_unsupported_type_with_guidance(
        self, client: TestClient, api: str, sign_in
    ):
        headers, _ = sign_in("9812350003")
        response = upload(
            client,
            api,
            headers,
            file=("notes.docx", io.BytesIO(b"PK\x03\x04"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        )
        assert response.status_code == 422
        assert "PNG" in response.json()["error"]["message"]

    def test_rejects_an_empty_file(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350004")
        response = upload(
            client, api, headers, file=("empty.png", io.BytesIO(b""), "image/png")
        )
        assert response.status_code == 422
        assert "empty" in response.json()["error"]["message"].lower()

    def test_rejects_a_file_over_the_limit(self, client: TestClient, api: str, sign_in):
        from app.config import settings

        headers, _ = sign_in("9812350005")
        oversized = b"\x89PNG\r\n\x1a\n" + b"0" * (settings.max_upload_bytes + 1)
        response = upload(
            client, api, headers, file=("big.png", io.BytesIO(oversized), "image/png")
        )
        assert response.status_code == 422
        assert "MB" in response.json()["error"]["message"]

    def test_requires_authentication(self, client: TestClient, api: str):
        response = client.post(
            f"{api}/patients/me/documents",
            files={"file": ("a.png", io.BytesIO(png_bytes()), "image/png")},
        )
        assert response.status_code == 401


class TestListing:
    def test_lists_newest_first(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350010")
        upload(client, api, headers, title="First")
        upload(client, api, headers, title="Second")
        body = client.get(f"{api}/patients/me/documents", headers=headers).json()
        assert body["total"] == 2
        assert [d["title"] for d in body["documents"]] == ["Second", "First"]

    def test_a_patient_only_sees_their_own(self, client: TestClient, api: str, sign_in):
        mine, _ = sign_in("9812350011")
        upload(client, api, mine, title="Mine")
        theirs, _ = sign_in("9812350012")
        body = client.get(f"{api}/patients/me/documents", headers=theirs).json()
        assert body["total"] == 0

    def test_the_stored_file_can_be_retrieved(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350013")
        document_id = upload(client, api, headers).json()["id"]
        response = client.get(
            f"{api}/patients/me/documents/{document_id}/file", headers=headers
        )
        assert response.status_code == 200
        assert response.content == png_bytes()

    def test_another_patient_cannot_retrieve_it(self, client: TestClient, api: str, sign_in):
        mine, _ = sign_in("9812350014")
        document_id = upload(client, api, mine).json()["id"]
        theirs, _ = sign_in("9812350015")
        response = client.get(
            f"{api}/patients/me/documents/{document_id}/file", headers=theirs
        )
        assert response.status_code == 404


class TestDeletion:
    def test_removes_the_record(self, client: TestClient, api: str, sign_in):
        headers, _ = sign_in("9812350020")
        document_id = upload(client, api, headers).json()["id"]
        body = client.delete(
            f"{api}/patients/me/documents/{document_id}", headers=headers
        ).json()
        assert body["total"] == 0

    def test_deleting_someone_elses_record_is_not_found(
        self, client: TestClient, api: str, sign_in
    ):
        mine, _ = sign_in("9812350021")
        document_id = upload(client, api, mine).json()["id"]
        theirs, _ = sign_in("9812350022")
        assert (
            client.delete(
                f"{api}/patients/me/documents/{document_id}", headers=theirs
            ).status_code
            == 404
        )


class TestLetterhead:
    """Reading who issued a document.

    A printed letterhead survives OCR even when the handwriting below it does
    not, so it is often the only structured information a scanned prescription
    yields. Every assertion here doubles as a statement about restraint: a
    wrong clinician name shown as fact is worse than a blank field.
    """

    def test_it_reads_a_printed_prescription(self):
        head = extraction.letterhead(
            "SHRI SAI POLYCLINIC\n"
            "Dr. A. R. Mehta, MBBS MD (Medicine)\n"
            "Date: 12/03/2026\n"
            "Diagnosis: Type 2 Diabetes Mellitus"
        )
        assert head["facility"] == "SHRI SAI POLYCLINIC"
        assert head["clinician"] == "Dr. A. R. Mehta"
        # The parenthetical is kept: "MD (Medicine)" says what the doctor
        # actually practises, which is the useful half.
        assert head["qualifications"] == "MBBS, MD (Medicine)"

    def test_it_reads_a_lab_report_and_a_department(self):
        assert extraction.letterhead("CITY DIAGNOSTIC LABORATORY\nNABL Accredited")[
            "facility"
        ] == "CITY DIAGNOSTIC LABORATORY"
        head = extraction.letterhead(
            "GOVERNMENT DISTRICT HOSPITAL\nOrthopaedics Out-patient Note"
        )
        assert head["department"] == "Orthopaedics Out-patient Note"

    def test_the_qualification_does_not_become_part_of_the_name(self):
        head = extraction.letterhead("APOLLO CLINIC\nDr. S Rao MBBS")
        assert head["clinician"] == "Dr. S Rao"
        assert head["qualifications"] == "MBBS"

    def test_a_patient_name_is_only_taken_from_a_label(self):
        # On a prescription the handwritten name is exactly what OCR mangles,
        # so an unlabelled line is never promoted to the patient's name.
        assert "patient_name" not in extraction.letterhead(
            "APOLLO CLINIC\nDr. S Rao MBBS\nSuresh Kumar\n01/08/2018"
        )
        head = extraction.letterhead(
            "APOLLO CLINIC\nDr. S Rao MBBS\nPatient Name: Suresh Kumar"
        )
        assert head["patient_name"] == "Suresh Kumar"

    def test_the_department_scan_does_not_swallow_other_lines(self):
        # "ent" lurks inside "Patient" and "Medicine" inside a qualification;
        # both used to be picked up as the department.
        head = extraction.letterhead(
            "APOLLO CLINIC\nDr. S Rao MBBS MD (Medicine)\nPatient Name: Suresh Kumar"
        )
        assert "department" not in head
        assert extraction.letterhead(
            "CITY ENT HOSPITAL\nDr. R Iyer MS\nENT Department"
        )["department"] == "ENT Department"

    def test_unreadable_handwriting_yields_nothing(self):
        """The real OCR output from a handwritten prescription.

        Nothing here is trustworthy, so nothing is claimed. This is the case
        that must never invent a doctor or a clinic.
        """
        head = extraction.letterhead(
            "m.Gopinatt\nMorning:Monday,Wedne\nSunday Closed\n818010\n"
            "ysnng\n1ay/ho\nP.veascolon\nOpC\nNochaua\nHfaspos\nloomg"
        )
        assert head == {}

    def test_it_survives_empty_and_junk_input(self):
        assert extraction.letterhead("") == {}
        assert extraction.letterhead("\n\n   \n") == {}

    def test_a_phone_number_is_read_when_present(self):
        head = extraction.letterhead("APOLLO CLINIC\nDr. S Rao\nPhone: 9848012345")
        assert head["phone"] == "9848012345"


class TestOcrEscalation:
    """A poor local read must not block the vision model.

    `run_ocr` used to return the local result the moment it was non-empty, so
    a page of garbage counted as a successful read and AiVisionProvider was
    never asked. Handwriting is exactly where that mattered: the local models
    are trained on print.
    """

    # The real RapidOCR output from a handwritten prescription.
    HANDWRITTEN = (
        "m.Gopinatt\nMorning:Monday,Wedne\nSunday Closed\n818010\nysnng\n"
        "1ay/ho\nP.veascolon\nOpC\nNochaua\nOap.\nx10cay\nHfaspos\nloomg\n"
        "Mom\nCouean\nCaeam\nanata\nMixocla\nx15da8\nhop"
    )
    PRINTED = (
        "SHRI SAI POLYCLINIC\nDr. A. R. Mehta, MBBS MD (Medicine)\n"
        "Date: 12/03/2026\nDiagnosis: Type 2 Diabetes Mellitus\nRx\n"
        "1. Tab. Metformin 500 mg  BD  x 30 days\nAdvice: Low salt diet"
    )

    def test_a_garbled_read_is_escalated(self):
        from app.services.ocr.provider import OcrResult, _looks_unreliable

        assert _looks_unreliable(
            OcrResult(text=self.HANDWRITTEN, engine="rapidocr", confidence=0.709)
        )

    def test_a_clean_printed_read_is_kept(self):
        """The common case must not pay for an API call it does not need."""
        from app.services.ocr.provider import OcrResult, _looks_unreliable

        assert not _looks_unreliable(
            OcrResult(text=self.PRINTED, engine="rapidocr", confidence=0.96)
        )

    def test_low_confidence_is_escalated_even_when_the_words_look_real(self):
        from app.services.ocr.provider import OcrResult, _looks_unreliable

        assert _looks_unreliable(
            OcrResult(text=self.PRINTED, engine="rapidocr", confidence=0.5)
        )

    def test_empty_or_wordless_text_is_escalated(self):
        from app.services.ocr.provider import OcrResult, _looks_unreliable

        for text in ("", "\n\n  \n", "12345 //// ---"):
            assert _looks_unreliable(
                OcrResult(text=text, engine="rapidocr", confidence=0.99)
            ), repr(text)

    async def test_the_local_result_still_wins_when_nothing_better_exists(
        self, tmp_path, monkeypatch
    ):
        """With no AI provider configured, a poor read is better than none.

        The document is never lost over this: a garbled transcription is still
        shown to the patient, and the file itself is always kept.
        """
        from app.services.ocr import provider as ocr

        monkeypatch.setattr(ocr.settings, "ocr_provider", "auto")
        garbled = ocr.OcrResult(
            text=self.HANDWRITTEN, engine="rapidocr", confidence=0.709
        )
        monkeypatch.setattr(
            ocr.LocalOcrProvider, "read", lambda *_args: garbled
        )

        # No AI provider configured, so escalation is attempted and declines.
        async def declines(*_args):
            return None

        monkeypatch.setattr(ocr.AiVisionProvider, "read_async", declines)
        image = tmp_path / "rx.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\n")
        result = await ocr.run_ocr(image, "image/png")
        assert result.engine == "rapidocr"
        assert result.text == self.HANDWRITTEN

    async def test_a_configured_vision_model_takes_over(self, tmp_path, monkeypatch):
        """The whole point: the better engine gets a turn."""
        from app.services.ocr import provider as ocr

        monkeypatch.setattr(ocr.settings, "ocr_provider", "auto")
        garbled = ocr.OcrResult(
            text=self.HANDWRITTEN, engine="rapidocr", confidence=0.709
        )
        monkeypatch.setattr(ocr.LocalOcrProvider, "read", lambda *_args: garbled)

        async def transcribes(*_args):
            return ocr.OcrResult(
                text="Dr. M. Gopinath MD(DVL)\nCap. Itaspor 200mg x 10 days",
                engine="ai_vision",
                confidence=0.85,
            )

        monkeypatch.setattr(ocr.AiVisionProvider, "read_async", transcribes)
        image = tmp_path / "rx.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\n")
        result = await ocr.run_ocr(image, "image/png")
        assert result.engine == "ai_vision"
        assert "Itaspor" in result.text

    async def test_a_clean_read_never_calls_the_vision_model(
        self, tmp_path, monkeypatch
    ):
        """Cost control: the common case must not hit an API."""
        from app.services.ocr import provider as ocr

        monkeypatch.setattr(ocr.settings, "ocr_provider", "auto")
        clean = ocr.OcrResult(text=self.PRINTED, engine="rapidocr", confidence=0.96)
        monkeypatch.setattr(ocr.LocalOcrProvider, "read", lambda *_args: clean)

        called = False

        async def must_not_run(*_args):
            nonlocal called
            called = True
            return None

        monkeypatch.setattr(ocr.AiVisionProvider, "read_async", must_not_run)
        image = tmp_path / "rx.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\n")
        result = await ocr.run_ocr(image, "image/png")
        assert result.engine == "rapidocr"
        assert called is False


class TestAFailedReadTellsThePatientNothingTechnical:
    """`processing_error` is shown to the patient, so it must stay plain.

    It used to be built as `f"{exc} ..."` where the exception text ended in
    the last provider's raw failure — so a Python `AttributeError`, or a
    vendor's JSON error body, could appear on a patient's records screen. The
    technical trail now travels on the exception separately, for the log.
    """

    @pytest.mark.asyncio
    async def test_the_message_is_plain_and_the_trail_is_separate(
        self, tmp_path, monkeypatch
    ):
        from app.services.ocr import provider as ocr_provider

        monkeypatch.setattr(ocr_provider.settings, "ocr_provider", "auto")

        def exploding_read(self, path, mime_type):  # noqa: ANN001
            raise AttributeError("'bytes' object has no attribute 'name'")

        async def no_vision(self, path, mime_type):  # noqa: ANN001
            return None

        monkeypatch.setattr(ocr_provider.LocalOcrProvider, "read", exploding_read)
        monkeypatch.setattr(ocr_provider.AiVisionProvider, "read_async", no_vision)

        image = tmp_path / "scan.jpg"
        image.write_bytes(b"\xff\xd8\xff\xdb not really a jpeg")

        with pytest.raises(ocr_provider.OcrUnavailable) as caught:
            await ocr_provider.run_ocr(image, "image/jpeg")

        patient_facing = str(caught.value)
        assert "AttributeError" not in patient_facing
        assert "bytes" not in patient_facing
        assert "object has no attribute" not in patient_facing

        # The detail still exists -- for whoever is reading the logs.
        assert "object has no attribute" in caught.value.technical

    @pytest.mark.asyncio
    async def test_a_silent_vision_failure_is_recorded(self, tmp_path, monkeypatch):
        """An exhausted quota must not be filed as "your photo was blurry"."""
        from app.services.ocr import provider as ocr_provider

        monkeypatch.setattr(ocr_provider.settings, "ocr_provider", "auto")
        monkeypatch.setattr(
            ocr_provider.LocalOcrProvider,
            "read",
            lambda self, path, mime_type: None,
        )

        async def no_vision(self, path, mime_type):  # noqa: ANN001
            return None

        monkeypatch.setattr(ocr_provider.AiVisionProvider, "read_async", no_vision)

        image = tmp_path / "scan.jpg"
        image.write_bytes(b"\xff\xd8\xff\xdb not really a jpeg")

        with pytest.raises(ocr_provider.OcrUnavailable) as caught:
            await ocr_provider.run_ocr(image, "image/jpeg")

        assert "ai_vision: returned no text" in caught.value.technical


class TestARealHandwrittenPrescription:
    """The exact vision-model transcription of a real handwritten slip.

    Kept verbatim because it is the document that motivated this work: the
    local engine read it as "m.Gopinatt / ysnng / 1ay/ho / P.veascolon". Two
    things it exposed are asserted here — a qualification set on its own line
    under the name, and a clinic number written as two groups of five.
    """

    TEXT = (
        "Dr. M. Gopinath\n"
        "MD(DVL)\n"
        "Timings: Morning: Monday, Wednesday & Friday\n"
        "Sunday Closed\n"
        "Clinic No.: 92480 02500 / 23222500 between 4-00 to 8-00 PM\n"
        "01/08/18\n"
        "Suresh\n"
        "19yrs/m\n"
        "DP. versicolor\n"
        "Rx\n"
        "(1) Cap. Itaspor 200mg x 10 days\n"
        "(2) Episcent cream for A Morn\n"
        "(3) Lamifin cream for A Night\n"
        "(4) Nizoclin Soap\n"
        "(5) Tab. Lejet/Safecet 5mg x 15 days\n"
        "R/A 15 days"
    )

    def test_the_clinician_and_speciality_are_read(self):
        head = extraction.letterhead(self.TEXT)
        assert head["clinician"] == "Dr. M. Gopinath"
        assert head["qualifications"] == "MD(DVL)"

    def test_the_clinic_number_is_read(self):
        assert extraction.letterhead(self.TEXT)["phone"] == "9248002500"

    def test_the_timings_line_is_not_mistaken_for_the_facility(self):
        head = extraction.letterhead(self.TEXT)
        assert "facility" not in head, "this slip names no clinic; a blank is correct"

    def test_the_patient_name_is_left_blank_rather_than_guessed(self):
        """"Suresh" is unlabelled, and a wrong name shown as fact is worse."""
        assert "patient_name" not in extraction.letterhead(self.TEXT)

    def test_the_date_is_read(self):
        assert str(extraction.document_date(self.TEXT)) == "2018-08-01"

    def test_it_is_recognised_as_a_prescription(self):
        assert extraction.detect_type(self.TEXT).value == "prescription"

    @pytest.mark.asyncio
    async def test_every_medicine_is_extracted(self):
        findings, _ = await extraction.extract(self.TEXT)
        medicines = {
            f.value for f in findings if f.entity_type.value == "medication"
        }
        assert "Itaspor" in medicines
        # Topical forms are medicines too; they were dropped before.
        assert "Episcent cream" in medicines
        assert "Lamifin cream" in medicines
        assert "Nizoclin Soap" in medicines
        assert "Lejet/Safecet" in medicines

    @pytest.mark.asyncio
    async def test_doses_and_durations_ride_along(self):
        findings, _ = await extraction.extract(self.TEXT)
        itaspor = next(f for f in findings if f.value == "Itaspor")
        assert itaspor.attributes["dose"] == "200 mg"
        assert itaspor.attributes["duration"] == "10 days"


class TestValuesAreFitToShowAPatient:
    """Two defects seen in real live output on the deployed API.

    Both were cosmetic in the sense that nothing crashed, and neither is
    cosmetic in the sense that matters: these strings are shown to a patient
    as what their prescription says, and to a clinician as the patient's
    record.
    """

    @pytest.mark.asyncio
    async def test_a_separator_is_not_part_of_the_medicine_name(self):
        """"Tab. Sucralfate - 10 ml TDS" gave the value "Sucralfate -"."""
        findings, _ = await extraction.extract(
            "Rx\n1) Tab. Sucralfate - 10 ml TDS x 10 days\n"
        )
        names = [f.value for f in findings if f.entity_type.value == "medication"]
        assert names == ["Sucralfate"]

    @pytest.mark.asyncio
    async def test_a_hyphen_inside_a_name_survives(self):
        findings, _ = await extraction.extract(
            "Rx\n1) Cap. Co-trimoxazole 480 mg BD x 5 days\n"
        )
        assert "Co-trimoxazole" in [f.value for f in findings]

    @pytest.mark.parametrize(
        "line,expected",
        [
            ("Patient: Nitin Jain Age: 34/M", "Nitin Jain"),
            ("Patient: Vikram Joshi        Age: 54 / M", "Vikram Joshi"),
            ("Name: A. R. Mehta | Age: 60", "A. R. Mehta"),
            ("Patient Name: Kamla Devi", "Kamla Devi"),
            ("Patient: Suresh", "Suresh"),
        ],
    )
    def test_the_name_stops_at_the_next_label(self, line, expected):
        """The whole remainder of the line used to be stored as the name."""
        assert extraction.letterhead(line)["patient_name"] == expected


class TestTheLocalEngineIsAnnouncedNotAssumed:
    """The local OCR engine needs ~700 MB once it has read a document.

    On a 512 MB instance the first upload gets the container OOM-killed,
    which surfaces as an HTTP health check failure with nothing pointing at
    OCR. A deployment that enables it should see the number in its logs.
    """

    @pytest.mark.parametrize("mode", ["auto", "local"])
    def test_it_warns_when_the_local_engine_is_enabled(self, mode, monkeypatch, caplog):
        from app import main
        from app.config import settings as live

        monkeypatch.setattr(live, "ocr_provider", mode)
        with caplog.at_level("WARNING", logger="medikiosk.startup"):
            main._warn_about_local_ocr_memory()
        assert any("OCR_PROVIDER" in record.message for record in caplog.records)

    @pytest.mark.parametrize("mode", ["ai", "off"])
    def test_it_stays_quiet_for_the_low_memory_settings(self, mode, monkeypatch, caplog):
        from app import main
        from app.config import settings as live

        monkeypatch.setattr(live, "ocr_provider", mode)
        with caplog.at_level("WARNING", logger="medikiosk.startup"):
            main._warn_about_local_ocr_memory()
        assert not caplog.records

    def test_the_ai_mode_never_touches_the_local_engine(self, monkeypatch):
        """That is the whole point: the 700 MB is the ONNX runtime."""
        from app.services.ocr import provider as ocr_provider

        monkeypatch.setattr(ocr_provider.settings, "ocr_provider", "ai")

        def explode(self, path, mime_type):  # noqa: ANN001
            raise AssertionError("the local engine must not be constructed")

        monkeypatch.setattr(ocr_provider.LocalOcrProvider, "read", explode)

        async def vision(self, path, mime_type):  # noqa: ANN001
            return ocr_provider.OcrResult(text="read", engine="ai_vision", confidence=0.85)

        monkeypatch.setattr(ocr_provider.AiVisionProvider, "read_async", vision)

        import asyncio
        from pathlib import Path

        result = asyncio.run(ocr_provider.run_ocr(Path("unused.jpg"), "image/jpeg"))
        assert result.engine == "ai_vision"
