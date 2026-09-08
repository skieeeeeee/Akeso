"""Previous medical records: stored in Phase 1, read in Phase 2."""

from __future__ import annotations

import io
import zlib

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
        assert head["qualifications"] == "MBBS, MD"

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
