"""Patient identity and personal-information use cases."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.patient.models import Patient
from app.modules.patient.onboarding import advance, progress_for
from app.modules.patient.schemas import PersonalInfoIn
from app.shared.enums import Language, OnboardingStatus
from app.shared.errors import NotFoundError
from app.shared.errors import ValidationFailedError as _ValidationFailedError
from app.shared.validators import normalize_mobile as _normalize_mobile


# Required before the personal-information step counts as finished.
REQUIRED_PERSONAL_FIELDS = ("full_name", "date_of_birth", "gender")


def has_required_personal_info(patient: Patient) -> bool:
    """Completeness is a property of the stored patient, not of one request.

    A multi-step form sends each field separately, so the final PATCH may
    carry only the last field while the patient record is now complete.
    """
    return all(getattr(patient, field) is not None for field in REQUIRED_PERSONAL_FIELDS)


def normalize_mobile(raw: str) -> str:
    """Service-boundary wrapper that maps a bad number onto a 422."""
    try:
        return _normalize_mobile(raw)
    except ValueError as exc:
        raise _ValidationFailedError(str(exc), details={"field": "mobile_number"}) from exc


def get_by_id(db: Session, patient_id: uuid.UUID) -> Patient:
    patient = db.get(Patient, patient_id)
    if patient is None:
        raise NotFoundError("Patient")
    return patient


def get_by_mobile(db: Session, mobile_number: str) -> Patient | None:
    return db.scalar(
        select(Patient).where(Patient.mobile_number == normalize_mobile(mobile_number))
    )


def load_full(db: Session, patient_id: uuid.UUID) -> Patient:
    """Patient with every related record eagerly loaded (profile screen)."""
    patient = db.scalar(
        select(Patient)
        .where(Patient.id == patient_id)
        .options(
            selectinload(Patient.abha_profile),
            selectinload(Patient.preferences),
            selectinload(Patient.consents),
            selectinload(Patient.assessments),
            selectinload(Patient.medical_profile),
            selectinload(Patient.documents),
            selectinload(Patient.encounters),
        )
    )
    if patient is None:
        raise NotFoundError("Patient")
    return patient


def get_or_create_by_mobile(
    db: Session, mobile_number: str, *, language: Language = Language.ENGLISH
) -> tuple[Patient, bool]:
    """Find or register a patient by mobile number.

    @returns (patient, created) — `created` drives first-time vs returning
    routing after login.
    """
    normalized = normalize_mobile(mobile_number)
    existing = db.scalar(select(Patient).where(Patient.mobile_number == normalized))
    if existing is not None:
        return existing, False

    patient = Patient(
        mobile_number=normalized,
        preferred_language=language,
        onboarding_status=OnboardingStatus.ABHA_PENDING,
    )
    db.add(patient)
    db.flush()
    return patient, True


def update_personal_info(db: Session, patient: Patient, payload: PersonalInfoIn) -> Patient:
    """Save whatever the patient has filled in so far.

    Called on every step of the multi-step form, so partial data is normal and
    must not be rejected. Onboarding advances only once the required fields
    are all present.
    """
    for field in (
        "full_name",
        "date_of_birth",
        "gender",
        "preferred_language",
        "emergency_contact_name",
        "emergency_contact_number",
        "emergency_contact_relation",
    ):
        value = getattr(payload, field)
        if value is not None:
            setattr(patient, field, value)

    # Keep the active interface language in step with the patient's choice.
    if payload.preferred_language is not None and patient.preferences is not None:
        patient.preferences.language = payload.preferred_language

    if has_required_personal_info(patient):
        patient.onboarding_status = advance(
            patient.onboarding_status, OnboardingStatus.PERSONAL_INFO_PENDING
        )

    db.flush()
    return patient


def mark_step_complete(db: Session, patient: Patient, step: OnboardingStatus) -> Patient:
    patient.onboarding_status = advance(patient.onboarding_status, step)
    db.flush()
    return patient


def progress(patient: Patient) -> dict[str, object]:
    p = progress_for(patient.onboarding_status)
    return {
        "status": p.status,
        "step_number": p.step_number,
        "total_steps": p.total_steps,
        "percent": p.percent,
        "next_route": p.next_route,
        "is_complete": p.is_complete,
    }
