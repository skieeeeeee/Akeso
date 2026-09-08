"""Authentication use cases: mocked OTP issue/verify, and demo sign-in."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.modules.auth.models import OtpChallenge
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.enums import Language
from app.shared.errors import (
    AuthenticationError,
    NotFoundError,
    ValidationFailedError,
    persist_before_raise,
)
from app.shared.security import (
    create_access_token,
    generate_otp,
    hash_otp,
    verify_otp,
)


def request_otp(db: Session, mobile_number: str) -> tuple[OtpChallenge, str]:
    """Issue a fresh OTP challenge.

    Only the hash is stored. The plain code is returned to the caller so the
    prototype can display it; a production build would hand it to an SMS
    gateway here instead and stop returning it.
    """
    # Supersede any outstanding challenge for this number.
    db.query(OtpChallenge).filter(
        OtpChallenge.mobile_number == mobile_number,
        OtpChallenge.consumed_at.is_(None),
    ).update({OtpChallenge.consumed_at: datetime.now(UTC)}, synchronize_session=False)

    # A fixed code, when the prototype is configured for one.
    code = settings.dev_fixed_otp or generate_otp()
    challenge = OtpChallenge(
        mobile_number=mobile_number,
        code_hash=hash_otp(mobile_number, code),
        expires_at=datetime.now(UTC) + timedelta(seconds=settings.otp_ttl_seconds),
    )
    db.add(challenge)
    db.flush()
    return challenge, code


def _active_challenge(db: Session, mobile_number: str) -> OtpChallenge:
    challenge = db.scalar(
        select(OtpChallenge)
        .where(
            OtpChallenge.mobile_number == mobile_number,
            OtpChallenge.consumed_at.is_(None),
        )
        .order_by(OtpChallenge.created_at.desc())
        .limit(1)
    )
    if challenge is None:
        raise AuthenticationError(
            "That code has expired. Please request a new one."
        )
    return challenge


def verify_and_sign_in(
    db: Session, mobile_number: str, code: str, language: Language
) -> tuple[Patient, bool]:
    challenge = _active_challenge(db, mobile_number)

    if challenge.expires_at <= datetime.now(UTC):
        challenge.consumed_at = datetime.now(UTC)
        persist_before_raise(db)
        raise AuthenticationError("That code has expired. Please request a new one.")

    if challenge.attempts >= settings.otp_max_attempts:
        challenge.consumed_at = datetime.now(UTC)
        persist_before_raise(db)
        raise AuthenticationError(
            "Too many incorrect attempts. Please request a new code."
        )

    if not verify_otp(mobile_number, code, challenge.code_hash):
        challenge.attempts += 1
        # Must outlive the error, or the lockout would never engage.
        persist_before_raise(db)
        remaining = max(0, settings.otp_max_attempts - challenge.attempts)
        raise AuthenticationError(
            f"That code is not correct. {remaining} attempt(s) left."
            if remaining
            else "Too many incorrect attempts. Please request a new code."
        )

    challenge.consumed_at = datetime.now(UTC)
    patient, created = patient_service.get_or_create_by_mobile(
        db, mobile_number, language=language
    )
    db.flush()
    return patient, created


def demo_sign_in(db: Session, demo_key: str) -> Patient:
    """Sign in as a seeded demo patient, identified by a stable key."""
    from app.modules.patient.demo import DEMO_PATIENTS  # local: avoids cycle

    definition = DEMO_PATIENTS.get(demo_key)
    if definition is None:
        raise ValidationFailedError(
            "That demo patient does not exist.", details={"field": "demo_key"}
        )
    patient = patient_service.get_by_mobile(db, definition.mobile_number)
    if patient is None:
        raise NotFoundError(
            "Demo patient",
            details={"hint": "Run `python -m app.cli seed` to create demo data."},
        )
    return patient


def issue_session(patient: Patient) -> tuple[str, int]:
    token = create_access_token(str(patient.id))
    return token, settings.access_token_ttl_minutes * 60
