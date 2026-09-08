"""Consent use cases."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.consent.content import CONSENT_TEXT_VERSION, REQUIRED_PURPOSES
from app.modules.consent.models import Consent
from app.modules.consent.schemas import ConsentSubmitIn
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.enums import ConsentPurpose, ConsentStatus, Language, OnboardingStatus
from app.shared.errors import NotFoundError, ValidationFailedError


def _current(db: Session, patient: Patient, purpose: ConsentPurpose) -> Consent | None:
    return db.scalar(
        select(Consent)
        .where(Consent.patient_id == patient.id, Consent.purpose == purpose)
        .order_by(Consent.created_at.desc())
        .limit(1)
    )


def active_consents(db: Session, patient: Patient) -> list[Consent]:
    """Latest record per purpose (a purpose can be granted, revoked, re-granted)."""
    latest: dict[ConsentPurpose, Consent] = {}
    rows = db.scalars(
        select(Consent)
        .where(Consent.patient_id == patient.id)
        .order_by(Consent.created_at.asc())
    ).all()
    for row in rows:
        latest[row.purpose] = row
    return list(latest.values())


def has_required_consents(db: Session, patient: Patient) -> bool:
    granted = {c.purpose for c in active_consents(db, patient) if c.is_active}
    return all(purpose in granted for purpose in REQUIRED_PURPOSES)


def submit(db: Session, patient: Patient, payload: ConsentSubmitIn) -> list[Consent]:
    """Record the patient's decisions.

    Declining a required purpose is allowed and recorded — it simply does not
    advance onboarding, because the health information cannot be collected
    without it.
    """
    now = datetime.now(UTC)
    language = Language(payload.language).value

    for decision in payload.decisions:
        existing = _current(db, patient, decision.purpose)
        # Re-deciding the same purpose supersedes the previous record rather
        # than editing it, so the history of decisions is preserved.
        if existing is not None and existing.status == (
            ConsentStatus.GRANTED if decision.granted else ConsentStatus.DECLINED
        ):
            continue

        db.add(
            Consent(
                patient_id=patient.id,
                purpose=decision.purpose,
                status=ConsentStatus.GRANTED if decision.granted else ConsentStatus.DECLINED,
                text_version=CONSENT_TEXT_VERSION,
                language=language,
                granted_at=now if decision.granted else None,
                declined_at=None if decision.granted else now,
            )
        )
    db.flush()

    if has_required_consents(db, patient):
        patient_service.mark_step_complete(db, patient, OnboardingStatus.CONSENT_PENDING)
        db.flush()

    return active_consents(db, patient)


def revoke(db: Session, patient: Patient, purpose: ConsentPurpose) -> Consent:
    existing = _current(db, patient, purpose)
    if existing is None:
        raise NotFoundError("Consent record")
    if existing.status != ConsentStatus.GRANTED:
        raise ValidationFailedError("That consent is not currently granted.")

    existing.status = ConsentStatus.REVOKED
    existing.revoked_at = datetime.now(UTC)
    db.flush()
    return existing
