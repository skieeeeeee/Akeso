"""Accessibility assessment and preference use cases."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.accessibility.models import (
    AccessibilityAssessment,
    PatientPreferences,
)
from app.modules.accessibility.recommendation import (
    AssessmentAnswers,
    EASY_MODE_THRESHOLD,
    Recommendation,
    recommend_experience,
)
from app.modules.accessibility.schemas import AssessmentIn, PreferencesIn
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.enums import (
    ContrastMode,
    FontSize,
    InteractionPreference,
    InterfaceMode,
    Language,
    OnboardingStatus,
    PreferenceSource,
)

# Defaults for a patient who has not taken the assessment yet. Deliberately
# the plain experience — nothing is assumed about them.
DEFAULT_PREFERENCES = {
    "interface_mode": InterfaceMode.STANDARD,
    "font_size": FontSize.NORMAL,
    "contrast_mode": ContrastMode.NORMAL,
    "audio_guidance": False,
    "interaction_preference": InteractionPreference.TOUCH,
}


def ensure_preferences(db: Session, patient: Patient) -> PatientPreferences:
    """Preferences always exist, so the UI never has to handle a null."""
    if patient.preferences is None:
        patient.preferences = PatientPreferences(
            patient_id=patient.id,
            language=patient.preferred_language,
            source=PreferenceSource.RECOMMENDED,
            **DEFAULT_PREFERENCES,
        )
        db.add(patient.preferences)
        db.flush()
    return patient.preferences


def _apply(preferences: PatientPreferences, recommendation: Recommendation) -> None:
    preferences.interface_mode = recommendation.interface_mode
    preferences.font_size = recommendation.font_size
    preferences.contrast_mode = recommendation.contrast_mode
    preferences.audio_guidance = recommendation.audio_guidance
    preferences.interaction_preference = recommendation.interaction_preference
    preferences.language = recommendation.language
    preferences.source = PreferenceSource.RECOMMENDED


def submit_assessment(
    db: Session, patient: Patient, payload: AssessmentIn
) -> tuple[AccessibilityAssessment, Recommendation, PatientPreferences]:
    """Record the answers, run the rule engine, pre-apply the result.

    The recommendation is applied immediately so the very next screen already
    renders in the recommended experience — but `source` stays RECOMMENDED
    until the patient confirms or customises it.
    """
    answers = AssessmentAnswers(
        digital_comfort=payload.digital_comfort,
        preferred_interaction=payload.preferred_interaction,
        reading_difficulty=payload.reading_difficulty,
        hearing_difficulty=payload.hearing_difficulty,
        vision_difficulty=payload.vision_difficulty,
        additional_needs=tuple(payload.additional_needs),
        age=patient.age,
        language=patient.preferred_language,
    )
    recommendation = recommend_experience(answers)

    assessment = AccessibilityAssessment(
        patient_id=patient.id,
        digital_comfort=payload.digital_comfort,
        preferred_interaction=payload.preferred_interaction,
        reading_difficulty=payload.reading_difficulty,
        hearing_difficulty=payload.hearing_difficulty,
        vision_difficulty=payload.vision_difficulty,
        additional_needs=[need.value for need in payload.additional_needs],
        additional_notes=payload.additional_notes,
        recommendation=recommendation.as_dict(),
        age_at_assessment=patient.age,
    )
    db.add(assessment)

    preferences = ensure_preferences(db, patient)
    _apply(preferences, recommendation)

    patient_service.mark_step_complete(db, patient, OnboardingStatus.ASSESSMENT_PENDING)
    db.flush()
    return assessment, recommendation, preferences


def update_preferences(
    db: Session, patient: Patient, payload: PreferencesIn
) -> PatientPreferences:
    """Accept the recommendation or customise it.

    Works during onboarding and at any time afterwards — a patient is never
    locked into a mode.
    """
    preferences = ensure_preferences(db, patient)

    changed = False
    for field in (
        "interface_mode",
        "font_size",
        "contrast_mode",
        "audio_guidance",
        "interaction_preference",
        "language",
    ):
        value = getattr(payload, field)
        if value is not None and value != getattr(preferences, field):
            setattr(preferences, field, value)
            changed = True

    # Keep the patient's language of record in step with the interface.
    if payload.language is not None:
        patient.preferred_language = Language(payload.language)

    preferences.source = (
        PreferenceSource.RECOMMENDED
        if payload.accepted_recommendation and not changed
        else PreferenceSource.CUSTOMIZED
    )

    patient_service.mark_step_complete(db, patient, OnboardingStatus.PREFERENCES_PENDING)
    db.flush()
    return preferences


def latest_recommendation(patient: Patient) -> dict | None:
    """The stored recommendation snapshot from the most recent assessment."""
    if not patient.assessments:
        return None
    snapshot = dict(patient.assessments[0].recommendation)
    snapshot.setdefault("easy_mode_threshold", EASY_MODE_THRESHOLD)
    return snapshot
