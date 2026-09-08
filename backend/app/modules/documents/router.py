"""Document endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.documents import service
from app.modules.documents import pipeline
from app.modules.documents.schemas import (
    DocumentListOut,
    DocumentOut,
    DocumentStatusOut,
    ExtractedItemOut,
    ReviewItemIn,
)
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared import storage
from app.shared.i18n import Localised, t
from app.shared.enums import DocumentType, ProcessingStatus
from app.shared.errors import NotFoundError

router = APIRouter(prefix="/patients/me/documents", tags=["documents"])


def _list_out(db: Session, patient: Patient) -> DocumentListOut:
    documents = service.list_for_patient(db, patient)
    progress = patient_service.progress(patient)
    return DocumentListOut(
        documents=[DocumentOut.model_validate(d) for d in documents],
        total=len(documents),
        onboarding_status=str(progress["status"]),
        next_route=str(progress["next_route"]),
    )


@router.get("", response_model=DocumentListOut)
def list_documents(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> DocumentListOut:
    return _list_out(db, patient)


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(DocumentType.OTHER),
    title: str | None = Form(None),
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentOut:
    """Store a previous medical record.

    The file is saved as-is. Reading its contents is Phase 2 work, so nothing
    here claims to have understood the document.
    """
    content = file.file.read()
    document = service.upload(
        db,
        patient,
        file_name=file.filename or "upload",
        mime_type=file.content_type or "application/octet-stream",
        content=content,
        document_type=document_type,
        title=title,
    )
    return DocumentOut.model_validate(document)


STATUS_MESSAGES: dict[str, Localised] = {
    "pending": t("Saved. Ready to be read.", "सहेजा गया। पढ़ने के लिए तैयार।"),
    "processing": t(
        "Reading your document. This usually takes a few seconds.",
        "आपका दस्तावेज़ पढ़ा जा रहा है। इसमें कुछ सेकंड लगते हैं।",
    ),
    "completed": t(
        "We found some information in this document. Please check it.",
        "हमें इस दस्तावेज़ में कुछ जानकारी मिली। कृपया इसे देखें।",
    ),
    "needs_review": t(
        "We read the text but could not pick out medical details. "
        "Your doctor can still read it.",
        "हमने टेक्स्ट पढ़ा पर चिकित्सीय विवरण नहीं निकाल सके। आपके डॉक्टर इसे पढ़ सकते हैं।",
    ),
    "failed": t(
        "We could not read this document. It is saved and you can try again.",
        "हम इस दस्तावेज़ को नहीं पढ़ सके। यह सहेजा गया है, आप फिर कोशिश कर सकते हैं।",
    ),
}


def _status_out(document) -> DocumentStatusOut:
    return DocumentStatusOut(
        id=document.id,
        processing_status=document.processing_status,
        processing_error=document.processing_error,
        finding_count=len(document.extracted_items),
        message=STATUS_MESSAGES.get(
            document.processing_status.value, STATUS_MESSAGES["pending"]
        ),
    )


@router.post("/{document_id}/process", response_model=DocumentOut)
async def process_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentOut:
    """Run OCR and extraction. Failure is reported as a state, not an error."""
    document = service.get(db, patient, document_id)
    return DocumentOut.model_validate(await pipeline.process(db, document))


@router.post("/{document_id}/retry", response_model=DocumentOut)
async def retry_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentOut:
    """Re-read a document. Findings a person already reviewed are kept."""
    document = service.get(db, patient, document_id)
    return DocumentOut.model_validate(await pipeline.retry(db, document))


@router.get("/{document_id}/status", response_model=DocumentStatusOut)
def document_status(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentStatusOut:
    return _status_out(service.get(db, patient, document_id))


@router.get("/{document_id}", response_model=DocumentOut)
def read_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentOut:
    return DocumentOut.model_validate(service.get(db, patient, document_id))


@router.post("/{document_id}/findings/{item_id}", response_model=ExtractedItemOut)
def review_finding(
    document_id: uuid.UUID,
    item_id: uuid.UUID,
    payload: ReviewItemIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> ExtractedItemOut:
    """Accept or reject one finding.

    Accepting records that a person agreed the document says this. It does not
    make it a confirmed diagnosis and does not alter the medical profile.
    """
    document = service.get(db, patient, document_id)
    row = pipeline.set_review_state(db, document, item_id, payload.review_state)
    return ExtractedItemOut.model_validate(row)


@router.get("/{document_id}/file")
def download_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> FileResponse:
    """Serve the stored file back to its owner."""
    document = service.get(db, patient, document_id)
    path = storage.absolute_path(document.file_path)
    if not path.exists():
        raise NotFoundError("Stored file")
    return FileResponse(path, media_type=document.mime_type, filename=document.file_name)


@router.delete("/{document_id}", response_model=DocumentListOut)
def delete_document(
    document_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> DocumentListOut:
    service.delete(db, patient, document_id)
    return _list_out(db, patient)
