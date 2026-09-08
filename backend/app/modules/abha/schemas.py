"""ABHA contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.shared.enums import AbhaVerificationStatus
from app.shared.schemas import ApiModel


class AbhaLinkIn(ApiModel):
    abha_id: str = Field(min_length=3, max_length=64)


class AbhaProfileOut(ApiModel):
    abha_id: str | None
    verification_status: AbhaVerificationStatus
    linked_at: datetime | None
    failure_reason: str | None
    # Always true in this build; surfaced so the UI can label it honestly.
    is_mock: bool


class AbhaStepOut(ApiModel):
    """Result of an ABHA step, including where onboarding goes next."""

    abha: AbhaProfileOut
    onboarding_status: str
    next_route: str
    # Set when the step succeeded but with a caveat the patient should see.
    notice: str | None = None
