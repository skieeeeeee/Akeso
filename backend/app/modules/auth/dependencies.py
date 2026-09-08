"""Request-scoped authentication dependencies."""

from __future__ import annotations

import uuid

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.errors import AuthenticationError
from app.shared.security import decode_access_token

# auto_error=False so a missing header produces our own JSON error shape
# rather than FastAPI's default.
_bearer = HTTPBearer(auto_error=False)


def current_patient(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> Patient:
    if credentials is None or not credentials.credentials:
        raise AuthenticationError("Please sign in to continue.")
    try:
        payload = decode_access_token(credentials.credentials)
        # A scoped token is a capability for one narrow thing — a visit
        # handoff link, say — and must never stand in for a session. Rejecting
        # it explicitly rather than relying on its subject failing to match a
        # patient row keeps that a rule instead of a coincidence.
        if payload.get("scope") is not None:
            raise AuthenticationError("Please sign in to continue.")
        patient_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise AuthenticationError("Your session has expired. Please sign in again.")

    return patient_service.get_by_id(db, patient_id)
