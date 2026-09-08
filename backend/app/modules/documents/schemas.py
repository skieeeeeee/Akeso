"""Document contracts."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from app.shared.enums import (
    DocumentType,
    ExtractedEntityType,
    LabFlag,
    ProcessingStatus,
    ReviewState,
)
from app.shared.schemas import ApiModel


class ExtractedItemOut(ApiModel):
    """A finding, not a fact. The UI must label it as such."""

    id: uuid.UUID
    entity_type: ExtractedEntityType
    value: str
    attributes: dict[str, str]
    numeric_value: str | None
    unit: str | None
    reference_range: str | None
    # Only present when a reference range was printed on the document.
    flag: LabFlag | None
    event_date: date | None
    confidence: float
    review_state: ReviewState
    extractor: str


class DocumentOut(ApiModel):
    id: uuid.UUID
    document_type: DocumentType
    title: str | None
    file_name: str
    mime_type: str
    size_bytes: int
    # PENDING in Phase 1: uploads are stored and shown to the clinician, but
    # OCR/extraction is Phase 2. Nothing claims to have read the document.
    processing_status: ProcessingStatus
    processing_error: str | None
    # Raw OCR text is kept even when extraction found nothing.
    ocr_text: str | None
    ocr_engine: str | None
    ocr_confidence: float | None
    document_date: date | None
    extracted_items: list[ExtractedItemOut] = []
    extracted_data: dict[str, Any] | None = None
    created_at: datetime


class DocumentListOut(ApiModel):
    documents: list[DocumentOut]
    total: int
    onboarding_status: str
    next_route: str


class DocumentStatusOut(ApiModel):
    """Lightweight polling shape while a document is being processed."""

    id: uuid.UUID
    processing_status: ProcessingStatus
    processing_error: str | None
    finding_count: int
    # Patient-facing explanation of what is happening right now.
    message: dict[str, str]


class ReviewItemIn(ApiModel):
    review_state: ReviewState
