"""Consent endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.consent import service
from app.modules.consent.content import (
    CONSENT_ITEMS,
    CONSENT_SUMMARY,
    CONSENT_TEXT_VERSION,
)
from app.modules.consent.schemas import (
    ConsentContentOut,
    ConsentOut,
    ConsentRevokeIn,
    ConsentStateOut,
    ConsentSubmitIn,
)
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient

router = APIRouter(prefix="/consents", tags=["consent"])


def _state(db: Session, patient: Patient) -> ConsentStateOut:
    progress = patient_service.progress(patient)
    return ConsentStateOut(
        consents=[ConsentOut.model_validate(c) for c in service.active_consents(db, patient)],
        has_required_consents=service.has_required_consents(db, patient),
        onboarding_status=str(progress["status"]),
        next_route=str(progress["next_route"]),
    )


@router.get("/content", response_model=ConsentContentOut)
def get_content() -> ConsentContentOut:
    """The consent text the patient must be shown, in every language."""
    return ConsentContentOut(
        version=CONSENT_TEXT_VERSION, summary=CONSENT_SUMMARY, items=CONSENT_ITEMS
    )


@router.get("", response_model=ConsentStateOut)
def list_consents(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> ConsentStateOut:
    return _state(db, patient)


@router.post("", response_model=ConsentStateOut)
def submit_consents(
    payload: ConsentSubmitIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> ConsentStateOut:
    service.submit(db, patient, payload)
    return _state(db, patient)


@router.post("/revoke", response_model=ConsentStateOut)
def revoke_consent(
    payload: ConsentRevokeIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> ConsentStateOut:
    service.revoke(db, patient, payload.purpose)
    return _state(db, patient)
