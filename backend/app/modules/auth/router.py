"""Authentication endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.modules.auth import service
from app.modules.auth.dependencies import current_patient
from app.modules.auth.schemas import (
    DemoLoginIn,
    DemoPatientOut,
    OtpRequestIn,
    OtpRequestOut,
    OtpVerifyIn,
    SessionOut,
)
from app.modules.patient import service as patient_service
from app.modules.patient.demo import demo_patient_list
from app.modules.patient.models import Patient
from app.modules.patient.schemas import PatientOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _session(patient: Patient, *, is_new: bool) -> SessionOut:
    token, ttl = service.issue_session(patient)
    return SessionOut(
        access_token=token,
        expires_in_seconds=ttl,
        patient=PatientOut.model_validate(patient),
        onboarding=patient_service.progress(patient),  # type: ignore[arg-type]
        is_new_patient=is_new,
    )


@router.post("/otp/request", response_model=OtpRequestOut)
def request_otp(payload: OtpRequestIn, db: Session = Depends(get_db)) -> OtpRequestOut:
    """Send a one-time code to the patient's mobile number.

    No SMS gateway is configured in the prototype, so the code is returned in
    the response and the UI presents it inside an explicit prototype notice.
    """
    challenge, code = service.request_otp(db, payload.mobile_number)
    return OtpRequestOut(
        mobile_number=payload.mobile_number,
        expires_at=challenge.expires_at,
        expires_in_seconds=settings.otp_ttl_seconds,
        is_prototype_delivery=settings.expose_mock_otp,
        prototype_code=code if settings.expose_mock_otp else None,
    )


@router.post("/otp/verify", response_model=SessionOut)
def verify_otp(payload: OtpVerifyIn, db: Session = Depends(get_db)) -> SessionOut:
    """Verify the code, creating the patient record on first sign-in."""
    patient, created = service.verify_and_sign_in(
        db, payload.mobile_number, payload.code, payload.language
    )
    return _session(patient, is_new=created)


@router.get("/demo-patients", response_model=list[DemoPatientOut])
def list_demo_patients() -> list[DemoPatientOut]:
    """The seeded fictional patients available for demonstration."""
    return [
        DemoPatientOut(
            demo_key=d.demo_key,
            label=d.label,
            description=d.description,
            mobile_number=d.mobile_number,
        )
        for d in demo_patient_list()
    ]


@router.post("/demo-login", response_model=SessionOut)
def demo_login(payload: DemoLoginIn, db: Session = Depends(get_db)) -> SessionOut:
    patient = service.demo_sign_in(db, payload.demo_key)
    return _session(patient, is_new=False)


@router.get("/me", response_model=SessionOut, status_code=status.HTTP_200_OK)
def me(patient: Patient = Depends(current_patient)) -> SessionOut:
    """Re-issues a token so a refreshed tab keeps its session."""
    return _session(patient, is_new=False)
