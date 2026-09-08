"""Patient API contracts."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Annotated

from pydantic import Field, field_validator

from app.shared.enums import CareSystem, Gender, Language, OnboardingStatus
from app.shared.schemas import ApiModel
from app.shared.validators import clean_text, normalize_mobile, validate_date_of_birth


class OnboardingProgressOut(ApiModel):
    status: OnboardingStatus
    step_number: int
    total_steps: int
    percent: int
    next_route: str
    is_complete: bool


class PatientOut(ApiModel):
    id: uuid.UUID
    full_name: str | None
    display_name: str
    mobile_number: str
    date_of_birth: date | None
    # Derived from date_of_birth — never stored.
    age: int | None
    gender: Gender | None
    preferred_language: Language
    emergency_contact_name: str | None
    emergency_contact_number: str | None
    emergency_contact_relation: str | None
    onboarding_status: OnboardingStatus
    # Pre-selected on the next visit so a returning patient is not asked cold.
    preferred_care_system: CareSystem | None
    is_demo: bool
    created_at: datetime


class PersonalInfoIn(ApiModel):
    """Every field optional so each step of the form can save as you go.

    Onboarding only advances once the required set is complete.
    """

    full_name: Annotated[str | None, Field(default=None, max_length=160)]
    date_of_birth: date | None = None
    gender: Gender | None = None
    preferred_language: Language | None = None
    emergency_contact_name: Annotated[str | None, Field(default=None, max_length=160)]
    emergency_contact_number: Annotated[str | None, Field(default=None, max_length=20)]
    emergency_contact_relation: Annotated[str | None, Field(default=None, max_length=60)]

    @field_validator("full_name", "emergency_contact_name", "emergency_contact_relation")
    @classmethod
    def _tidy(cls, value: str | None) -> str | None:
        cleaned = clean_text(value, max_length=160)
        return cleaned

    @field_validator("date_of_birth")
    @classmethod
    def _check_dob(cls, value: date | None) -> date | None:
        return validate_date_of_birth(value) if value else None

    @field_validator("emergency_contact_number")
    @classmethod
    def _check_contact(cls, value: str | None) -> str | None:
        return normalize_mobile(value) if value else None


class AbhaSummary(ApiModel):
    abha_id: str | None
    verification_status: str
    linked_at: datetime | None
    failure_reason: str | None
    is_mock: bool


class PreferencesSummary(ApiModel):
    interface_mode: str
    font_size: str
    contrast_mode: str
    audio_guidance: bool
    interaction_preference: str
    language: str
    source: str


class ConsentSummary(ApiModel):
    purpose: str
    status: str
    granted_at: datetime | None
    revoked_at: datetime | None


class MedicalProfileCounts(ApiModel):
    """Per-section counts so the profile UI can show real content, not stubs."""

    sections: dict[str, int]
    total_items: int


class PatientProfileOut(ApiModel):
    """Everything the patient profile screen needs in one request."""

    patient: PatientOut
    onboarding: OnboardingProgressOut
    abha: AbhaSummary | None
    preferences: PreferencesSummary | None
    consents: list[ConsentSummary]
    medical_profile: MedicalProfileCounts
    document_count: int
    encounter_count: int
    last_assessment_at: datetime | None
