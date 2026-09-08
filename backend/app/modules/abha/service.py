"""ABHA linking use cases.

Failure isolation: nothing here can stop onboarding. A bad identifier, a
rejected identifier or an unavailable registry all leave the patient able to
continue — the attempt and its reason are recorded on the profile.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.modules.abha import mock_registry
from app.modules.abha.models import AbhaProfile
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.enums import AbhaVerificationStatus, OnboardingStatus
from app.shared.errors import (
    UpstreamUnavailableError,
    ValidationFailedError,
    persist_before_raise,
)


def _profile_for(db: Session, patient: Patient) -> AbhaProfile:
    if patient.abha_profile is None:
        patient.abha_profile = AbhaProfile(patient_id=patient.id, is_mock=True)
        db.add(patient.abha_profile)
        db.flush()
    return patient.abha_profile


def get_profile(db: Session, patient: Patient) -> AbhaProfile:
    return _profile_for(db, patient)


def link(db: Session, patient: Patient, raw_abha_id: str) -> AbhaProfile:
    """Attempt to link an ABHA identifier (mock verification).

    The entered value is always preserved on the profile so the patient never
    has to retype it after a failure.
    """
    profile = _profile_for(db, patient)
    # What the patient actually typed. Kept verbatim on any unsuccessful
    # outcome so the field they see still shows their own input; only a
    # verified id is stored in normalised form.
    entered = (raw_abha_id or "").strip()

    try:
        result = mock_registry.verify(raw_abha_id)
    except mock_registry.RegistryUnavailable as exc:
        profile.abha_id = entered
        profile.verification_status = AbhaVerificationStatus.UNVERIFIED
        profile.failure_reason = (
            "We could not reach the health ID service. You can continue and link it later."
        )
        # Keep what the patient typed so they never have to retype it.
        persist_before_raise(db)
        raise UpstreamUnavailableError(profile.failure_reason) from exc

    if not result.verified:
        profile.abha_id = entered
        profile.verification_status = AbhaVerificationStatus.FAILED
        profile.failure_reason = result.reason
        persist_before_raise(db)
        raise ValidationFailedError(
            result.reason or "This health ID could not be verified.",
            details={"field": "abha_id"},
        )

    profile.abha_id = result.normalized_id
    profile.verification_status = AbhaVerificationStatus.VERIFIED
    profile.failure_reason = None
    profile.linked_at = datetime.now(UTC)
    patient_service.mark_step_complete(db, patient, OnboardingStatus.ABHA_PENDING)
    db.flush()
    return profile


def skip(db: Session, patient: Patient) -> AbhaProfile:
    """Continue without a health ID. Always available."""
    profile = _profile_for(db, patient)
    if profile.verification_status != AbhaVerificationStatus.VERIFIED:
        profile.verification_status = AbhaVerificationStatus.SKIPPED
        profile.failure_reason = None
    patient_service.mark_step_complete(db, patient, OnboardingStatus.ABHA_PENDING)
    db.flush()
    return profile
