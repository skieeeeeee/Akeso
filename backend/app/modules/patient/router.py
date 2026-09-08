"""Patient profile endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS
from app.modules.patient import home as home_builder
from app.modules.patient import service
from app.modules.patient.models import Patient
from app.modules.patient.schemas import (
    OnboardingProgressOut,
    PatientOut,
    PatientProfileOut,
    PersonalInfoIn,
)
from app.shared.schemas import ApiModel

router = APIRouter(prefix="/patients", tags=["patient"])


@router.get("/me", response_model=PatientOut)
def get_me(patient: Patient = Depends(current_patient)) -> Patient:
    return patient


@router.patch("/me", response_model=PatientOut)
def update_me(
    payload: PersonalInfoIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> Patient:
    """Save personal information.

    Accepts partial data so each step of the multi-step form can persist as
    the patient moves forward and backward without losing anything.
    """
    return service.update_personal_info(db, patient, payload)


@router.get("/me/profile", response_model=PatientProfileOut)
def get_profile(
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> PatientProfileOut:
    """Everything the profile screen renders, in one request."""
    full = service.load_full(db, patient.id)
    profile = full.medical_profile

    sections = {
        name: len(profile.section(name)) if profile else 0
        for name in MEDICAL_PROFILE_SECTIONS
    }

    return PatientProfileOut(
        patient=PatientOut.model_validate(full),
        onboarding=service.progress(full),  # type: ignore[arg-type]
        abha=full.abha_profile,  # type: ignore[arg-type]
        preferences=full.preferences,  # type: ignore[arg-type]
        consents=full.consents,  # type: ignore[arg-type]
        medical_profile={  # type: ignore[arg-type]
            "sections": sections,
            "total_items": sum(sections.values()),
        },
        document_count=len(full.documents),
        encounter_count=len(full.encounters),
        last_assessment_at=full.assessments[0].created_at if full.assessments else None,
    )


class HomeOut(ApiModel):
    """Everything the returning-patient home screen renders, in one call."""

    patient: PatientOut
    greeting: dict[str, str]
    onboarding: OnboardingProgressOut
    profile_complete: bool
    history_item_count: int
    conditions: list[str]
    medications: list[str]
    allergies: list[str]
    recent_documents: list[dict[str, Any]]
    document_count: int
    recent_events: list[dict[str, Any]]
    last_visit: dict[str, Any] | None
    visit_count: int
    visit_in_progress: dict[str, Any] | None


@router.get("/me/home", response_model=HomeOut)
def get_home(
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> HomeOut:
    """The personalised home screen for a recognised patient."""
    return HomeOut.model_validate(home_builder.build(db, patient))
