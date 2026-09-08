"""Previous medical records uploaded by the patient.

Phase 1 stores and lists them. OCR + extraction (`processing_status`,
`ocr_text`, `extracted_data`) is Phase 2 — the columns exist now so an upload
made today is processable later without a migration.
"""

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import enum_column
from app.shared.enums import (
    DocumentType,
    ExtractedEntityType,
    LabFlag,
    ProcessingStatus,
    ReviewState,
)

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.encounter.models import Encounter
    from app.modules.patient.models import Patient


class Document(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    encounter_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("encounters.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        enum_column(DocumentType, "document_type"),
        nullable=False,
        default=DocumentType.OTHER,
        server_default=DocumentType.OTHER.value,
    )
    title: Mapped[str | None] = mapped_column(sa.String(200), nullable=True)
    file_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    # Path relative to the configured upload directory.
    file_path: Mapped[str] = mapped_column(sa.String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    size_bytes: Mapped[int] = mapped_column(sa.Integer(), nullable=False, default=0)

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        enum_column(ProcessingStatus, "processing_status"),
        nullable=False,
        default=ProcessingStatus.PENDING,
        server_default=ProcessingStatus.PENDING.value,
    )
    ocr_text: Mapped[str | None] = mapped_column(sa.Text(), nullable=True)
    ocr_engine: Mapped[str | None] = mapped_column(sa.String(40), nullable=True)
    ocr_confidence: Mapped[float | None] = mapped_column(sa.Float(), nullable=True)
    extracted_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    processing_error: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)

    # Date printed on the document, used to place it on the timeline.
    document_date: Mapped[date | None] = mapped_column(sa.Date(), nullable=True)

    patient: Mapped["Patient"] = relationship(back_populates="documents")
    encounter: Mapped["Encounter | None"] = relationship(back_populates="documents")
    extracted_items: Mapped[list["ExtractedMedicalData"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="ExtractedMedicalData.entity_type",
    )


class ExtractedMedicalData(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One clinical entity found in a document.

    Deliberately a *finding*, not a fact: `review_state` starts UNREVIEWED and
    the UI presents these as "information found in this document" rather than
    as confirmed diagnoses. Nothing here is copied into the medical profile
    until a person accepts it.
    """

    __tablename__ = "extracted_medical_data"

    document_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entity_type: Mapped[ExtractedEntityType] = mapped_column(
        enum_column(ExtractedEntityType, "extracted_entity_type"), nullable=False, index=True
    )
    value: Mapped[str] = mapped_column(sa.String(300), nullable=False)
    # Medication dose/frequency, procedure site, etc.
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )

    # Investigation specifics. `flag` is only ever computed from a printed
    # reference range — never inferred.
    numeric_value: Mapped[str | None] = mapped_column(sa.String(40), nullable=True)
    unit: Mapped[str | None] = mapped_column(sa.String(40), nullable=True)
    reference_range: Mapped[str | None] = mapped_column(sa.String(80), nullable=True)
    flag: Mapped[LabFlag | None] = mapped_column(
        enum_column(LabFlag, "lab_flag"), nullable=True
    )

    event_date: Mapped[date | None] = mapped_column(sa.Date(), nullable=True)
    confidence: Mapped[float] = mapped_column(
        sa.Float(), nullable=False, default=0.5, server_default="0.5"
    )
    review_state: Mapped[ReviewState] = mapped_column(
        enum_column(ReviewState, "review_state"),
        nullable=False,
        default=ReviewState.UNREVIEWED,
        server_default=ReviewState.UNREVIEWED.value,
    )
    # Which engine produced it, so a low-confidence run can be re-done.
    extractor: Mapped[str] = mapped_column(
        sa.String(40), nullable=False, default="rules", server_default="rules"
    )

    document: Mapped["Document"] = relationship(back_populates="extracted_items")
