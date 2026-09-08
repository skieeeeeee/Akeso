"""Token issuing/verification and OTP hashing."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.config import settings

_ALGO = settings.jwt_algorithm


def create_access_token(patient_id: str, *, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": patient_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.access_token_ttl_minutes)).timestamp()),
        "iss": settings.app_name,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGO)


def decode_access_token(token: str) -> dict[str, Any]:
    """@raises jwt.PyJWTError when the token is invalid or expired."""
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[_ALGO],
        issuer=settings.app_name,
        options={"require": ["exp", "sub"]},
    )


def generate_otp(digits: int = 6) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(digits))


def hash_otp(mobile_number: str, code: str) -> str:
    """Salted with the mobile number so codes are not interchangeable."""
    return hashlib.sha256(
        f"{settings.jwt_secret}:{mobile_number}:{code}".encode()
    ).hexdigest()


def verify_otp(mobile_number: str, code: str, code_hash: str) -> bool:
    return hmac.compare_digest(hash_otp(mobile_number, code), code_hash)


# A handoff token is not a session. It grants read-only access to exactly one
# visit summary, for as long as a consultation lasts, to whoever holds the
# link — which is the point: the clinician scanning it has no account here.
# The scope claim is what keeps the two apart, and `current_patient` refuses
# any token that carries one.
HANDOFF_SCOPE = "visit_handoff"


def create_handoff_token(encounter_id: str) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": encounter_id,
        "scope": HANDOFF_SCOPE,
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(minutes=settings.handoff_link_ttl_minutes)).timestamp()
        ),
        "iss": settings.app_name,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=_ALGO)


def decode_handoff_token(token: str) -> str:
    """@returns the encounter id this token may read.

    @raises jwt.PyJWTError when the token is invalid, expired, or is not a
            handoff token — a patient session must never be usable here
            either, or a leaked link would widen into a whole account.
    """
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[_ALGO],
        issuer=settings.app_name,
        options={"require": ["exp", "sub"]},
    )
    if payload.get("scope") != HANDOFF_SCOPE:
        raise jwt.InvalidTokenError("not a visit handoff token")
    return str(payload["sub"])
