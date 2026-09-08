"""Accessibility endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.accessibility import service
from app.modules.accessibility.content import ASSESSMENT_QUESTIONS, PREFERENCE_OPTIONS
from app.modules.accessibility.schemas import (
    AssessmentContentOut,
    AssessmentIn,
    AssessmentResultOut,
    PreferencesIn,
    PreferencesOut,
    RecommendationOut,
)
from app.modules.auth.dependencies import current_patient
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient

router = APIRouter(prefix="/accessibility", tags=["accessibility"])


@router.get("/content", response_model=AssessmentContentOut)
def get_content() -> AssessmentContentOut:
    """Assessment questions and preference labels, in every language.

    Served from the API so the two clients cannot drift out of sync.
    """
    return AssessmentContentOut(
        questions=ASSESSMENT_QUESTIONS, preference_options=PREFERENCE_OPTIONS
    )


@router.post("/assessment", response_model=AssessmentResultOut)
def submit_assessment(
    payload: AssessmentIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> AssessmentResultOut:
    """Score the assessment with the deterministic rule engine."""
    assessment, recommendation, preferences = service.submit_assessment(
        db, patient, payload
    )
    progress = patient_service.progress(patient)
    return AssessmentResultOut(
        assessment_id=str(assessment.id),
        recommendation=RecommendationOut.model_validate(recommendation.as_dict()),
        preferences=PreferencesOut.model_validate(preferences),
        onboarding_status=str(progress["status"]),
        next_route=str(progress["next_route"]),
    )


@router.get("/preferences", response_model=PreferencesOut)
def get_preferences(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> PreferencesOut:
    return PreferencesOut.model_validate(service.ensure_preferences(db, patient))


@router.put("/preferences", response_model=PreferencesOut)
def put_preferences(
    payload: PreferencesIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> PreferencesOut:
    """Accept or change the experience. Available during and after onboarding."""
    return PreferencesOut.model_validate(service.update_preferences(db, patient, payload))


@router.get("/recommendation", response_model=RecommendationOut | None)
def get_recommendation(patient: Patient = Depends(current_patient)) -> RecommendationOut | None:
    """The most recent recommendation snapshot, if the assessment was taken."""
    snapshot = service.latest_recommendation(patient)
    return RecommendationOut.model_validate(snapshot) if snapshot else None
