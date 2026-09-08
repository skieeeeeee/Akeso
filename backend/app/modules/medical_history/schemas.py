"""Medical profile contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field, field_validator

from app.shared.clinical import ClinicalItem
from app.shared.schemas import ApiModel
from app.shared.validators import clean_text


class MedicalItemIn(ApiModel):
    """One fact as typed by the patient during onboarding."""

    value: str = Field(min_length=1, max_length=300)
    attributes: dict[str, str] = Field(default_factory=dict)
    note: str | None = Field(default=None, max_length=500)

    @field_validator("value", "note")
    @classmethod
    def _tidy(cls, value: str | None) -> str | None:
        return clean_text(value, max_length=500)


class MedicalProfileIn(ApiModel):
    """Sections to replace. Omitted sections are left untouched.

    Replacing a whole section (rather than patching items) keeps the
    add/remove interaction on the client simple and idempotent.
    """

    sections: dict[str, list[MedicalItemIn]] = Field(default_factory=dict)

    @field_validator("sections")
    @classmethod
    def _known_sections(cls, value: dict[str, Any]) -> dict[str, Any]:
        from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS

        unknown = set(value) - set(MEDICAL_PROFILE_SECTIONS)
        if unknown:
            raise ValueError(f"Unknown medical section(s): {', '.join(sorted(unknown))}")
        return value


class MedicalProfileOut(ApiModel):
    sections: dict[str, list[ClinicalItem]]
    total_items: int
    updated_at: datetime | None
    onboarding_status: str
    next_route: str


class MedicalContentOut(ApiModel):
    sections: list[dict[str, Any]]
