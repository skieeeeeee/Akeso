"""The document processing pipeline.

    stored -> processing -> OCR -> raw text -> extraction -> findings -> review

The invariants that matter:

* The file is stored before processing begins, and is never deleted because a
  later stage failed.
* Each stage failure is recorded as a *state*, not an exception: `failed` when
  no text could be read, `needs_review` when text was read but nothing
  structured came out of it. The raw OCR text is kept either way.
* Nothing here writes to the patient's medical profile. Findings are
  presented as "information found in this document" for a person to accept.
"""

from __future__ import annotations

import logging
import uuid

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.modules.documents import extraction
from app.modules.documents.models import Document, ExtractedMedicalData
from app.services.ocr import OcrUnavailable, run_ocr
from app.shared import storage
from app.shared.enums import ProcessingStatus, ReviewState
from app.shared.errors import NotFoundError

log = logging.getLogger("medikiosk.documents.pipeline")


async def process(db: Session, document: Document) -> Document:
    """Run OCR then extraction. Never raises for a pipeline failure."""
    document.processing_status = ProcessingStatus.PROCESSING
    document.processing_error = None
    db.flush()

    path = storage.absolute_path(document.file_path)
    if not path.exists():
        # The record outlived its file; say so plainly rather than retrying.
        document.processing_status = ProcessingStatus.FAILED
        document.processing_error = (
            "The stored file could not be found. Please upload it again."
        )
        db.flush()
        return document

    # --- OCR ---------------------------------------------------------------
    try:
        result = await run_ocr(path, document.mime_type)
    except OcrUnavailable as exc:
        # The technical trail goes to the log; only the plain sentence goes
        # into `processing_error`, which the patient reads.
        log.info(
            "OCR unavailable for %s: %s (%s)",
            document.id,
            exc,
            getattr(exc, "technical", None) or "no detail",
        )
        document.processing_status = ProcessingStatus.FAILED
        document.processing_error = (
            f"{exc} Your document is saved and your doctor can still see it. "
            "You can try again at any time."
        )
        db.flush()
        return document
    except Exception as exc:  # noqa: BLE001 - an engine crash is not a lost document
        log.warning("OCR crashed for %s: %s", document.id, exc)
        document.processing_status = ProcessingStatus.FAILED
        document.processing_error = (
            "We could not read this document. It is saved and can be retried."
        )
        db.flush()
        return document

    document.ocr_text = result.text
    document.ocr_engine = result.engine
    document.ocr_confidence = result.confidence
    document.document_date = extraction.document_date(result.text) or document.document_date
    # Who issued the document. A printed letterhead reads reliably even when
    # the handwriting under it does not, so this is often the only structured
    # information a scanned prescription yields.
    header = extraction.letterhead(result.text)
    document.extracted_data = {**(document.extracted_data or {}), "letterhead": header}
    detected = extraction.detect_type(result.text)
    if detected.value != "other":
        document.document_type = detected
    db.flush()

    # --- Extraction --------------------------------------------------------
    try:
        findings, extractor = await extraction.extract(result.text)
    except Exception as exc:  # noqa: BLE001
        log.warning("extraction crashed for %s: %s", document.id, exc)
        document.processing_status = ProcessingStatus.NEEDS_REVIEW
        document.processing_error = (
            "We read the text but could not pick out the medical details. "
            "The text is saved for your doctor."
        )
        db.flush()
        return document

    # Re-processing replaces previous findings rather than duplicating them,
    # but only findings nobody has reviewed yet.
    db.execute(
        delete(ExtractedMedicalData).where(
            ExtractedMedicalData.document_id == document.id,
            ExtractedMedicalData.review_state == ReviewState.UNREVIEWED,
        )
    )
    db.flush()

    reviewed = {
        (row.entity_type.value, row.value.strip().lower())
        for row in document.extracted_items
        if row.review_state != ReviewState.UNREVIEWED
    }
    added = 0
    for finding in findings:
        if finding.dedupe_key in reviewed:
            continue
        db.add(
            ExtractedMedicalData(
                document_id=document.id,
                entity_type=finding.entity_type,
                value=finding.value[:300],
                attributes=finding.attributes,
                numeric_value=finding.numeric_value,
                unit=finding.unit,
                reference_range=finding.reference_range,
                flag=finding.flag,
                event_date=finding.event_date or document.document_date,
                confidence=finding.confidence,
                extractor=extractor,
            )
        )
        added += 1

    if added == 0 and not reviewed:
        document.processing_status = ProcessingStatus.NEEDS_REVIEW
        document.processing_error = (
            "We read the text but did not find medical details we recognise. "
            "Your doctor can still read the document."
        )
    else:
        document.processing_status = ProcessingStatus.COMPLETED
        document.processing_error = None

    db.flush()
    # The rows were added to the session, not to the loaded collection; refresh
    # so the caller (and the API response) sees them.
    db.refresh(document, attribute_names=["extracted_items"])
    log.info("processed %s: %s finding(s) via %s", document.id, added, extractor)
    return document


async def retry(db: Session, document: Document) -> Document:
    """Re-run the pipeline. Reviewed findings are preserved."""
    return await process(db, document)


def set_review_state(
    db: Session, document: Document, item_id: uuid.UUID, state: ReviewState
) -> ExtractedMedicalData:
    """Accept or reject one finding.

    Accepting records that a person agreed the document says this — it is
    still not a confirmed diagnosis, and nothing is copied into the medical
    profile automatically.
    """
    row = next((item for item in document.extracted_items if item.id == item_id), None)
    if row is None:
        raise NotFoundError("Extracted item")
    row.review_state = state
    db.flush()
    return row
