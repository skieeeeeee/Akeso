"""Consent contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from app.shared.enums import ConsentPurpose, ConsentStatus, Language
from app.shared.schemas import ApiModel


class ConsentDecisionIn(ApiModel):
    purpose: ConsentPurpose
    granted: bool


class ConsentSubmitIn(ApiModel):
    decisions: list[ConsentDecisionIn] = Field(min_length=1)
    language: Language = Language.ENGLISH


class ConsentOut(ApiModel):
    purpose: ConsentPurpose
    status: ConsentStatus
    text_version: str
    language: str
    granted_at: datetime | None
    declined_at: datetime | None
    revoked_at: datetime | None
    is_active: bool


class ConsentStateOut(ApiModel):
    consents: list[ConsentOut]
    # True once every required purpose is granted.
    has_required_consents: bool
    onboarding_status: str
    next_route: str


class ConsentContentOut(ApiModel):
    version: str
    summary: dict[str, Any]
    items: list[dict[str, Any]]


class ConsentRevokeIn(ApiModel):
    purpose: ConsentPurpose
