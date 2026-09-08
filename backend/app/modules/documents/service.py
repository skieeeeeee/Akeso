"""Document use cases (Phase 1: store and list)."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.documents.models import Document
from app.modules.patient.models import Patient
from app.shared import storage
from app.shared.enums import DocumentType, ProcessingStatus
from app.shared.errors import NotFoundError


def upload(
    db: Session,
    patient: Patient,
    *,
    file_name: str,
    mime_type: str,
    content: bytes,
    document_type: DocumentType = DocumentType.OTHER,
    title: str | None = None,
) -> Document:
    storage.validate_upload(mime_type, len(content))
    relative_path = storage.save(patient.id, file_name, content)

    document = Document(
        patient_id=patient.id,
        document_type=document_type,
        title=title,
        file_name=storage.safe_name(file_name),
        file_path=relative_path,
        mime_type=mime_type,
        size_bytes=len(content),
        # Phase 2 moves this to PROCESSING and fills in the OCR fields.
        processing_status=ProcessingStatus.PENDING,
    )
    db.add(document)
    db.flush()
    return document


def list_for_patient(db: Session, patient: Patient) -> list[Document]:
    return list(
        db.scalars(
            select(Document)
            .where(Document.patient_id == patient.id)
            .order_by(Document.created_at.desc())
        ).all()
    )


def get(db: Session, patient: Patient, document_id: uuid.UUID) -> Document:
    document = db.scalar(
        select(Document).where(
            Document.id == document_id, Document.patient_id == patient.id
        )
    )
    if document is None:
        raise NotFoundError("Document")
    return document


def delete(db: Session, patient: Patient, document_id: uuid.UUID) -> None:
    document = get(db, patient, document_id)
    storage.delete(document.file_path)
    db.delete(document)
    db.flush()
