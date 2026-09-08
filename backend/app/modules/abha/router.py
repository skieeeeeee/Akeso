"""ABHA endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.abha import service
from app.modules.abha.schemas import AbhaLinkIn, AbhaProfileOut, AbhaStepOut
from app.modules.auth.dependencies import current_patient
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient

router = APIRouter(prefix="/patients/me/abha", tags=["abha"])


def _step(patient: Patient, profile, notice: str | None = None) -> AbhaStepOut:
    progress = patient_service.progress(patient)
    return AbhaStepOut(
        abha=AbhaProfileOut.model_validate(profile),
        onboarding_status=str(progress["status"]),
        next_route=str(progress["next_route"]),
        notice=notice,
    )


@router.get("", response_model=AbhaProfileOut)
def get_abha(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> AbhaProfileOut:
    return AbhaProfileOut.model_validate(service.get_profile(db, patient))


@router.post("/link", response_model=AbhaStepOut)
def link_abha(
    payload: AbhaLinkIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> AbhaStepOut:
    """Link a health ID using mock verification (no ABDM call is made)."""
    profile = service.link(db, patient, payload.abha_id)
    return _step(patient, profile)


@router.post("/skip", response_model=AbhaStepOut)
def skip_abha(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> AbhaStepOut:
    """Continue onboarding without linking a health ID."""
    profile = service.skip(db, patient)
    return _step(
        patient,
        profile,
        notice="You can link your health ID later from your profile.",
    )
