"""Authentication contracts."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from app.modules.patient.schemas import OnboardingProgressOut, PatientOut
from app.shared.enums import Language
from app.shared.i18n import Localised
from app.shared.schemas import ApiModel
from app.shared.validators import normalize_mobile


class OtpRequestIn(ApiModel):
    # Length is deliberately permissive: `normalize_mobile` produces the
    # patient-facing message for anything that is not a valid number.
    mobile_number: str = Field(max_length=20)
    language: Language = Language.ENGLISH

    @field_validator("mobile_number")
    @classmethod
    def _normalize(cls, value: str) -> str:
        return normalize_mobile(value)


class OtpRequestOut(ApiModel):
    mobile_number: str
    expires_at: datetime
    expires_in_seconds: int
    # True when the API is returning the code directly because no SMS gateway
    # is configured. The UI must label this as prototype behaviour.
    is_prototype_delivery: bool
    prototype_code: str | None = None


class OtpVerifyIn(ApiModel):
    mobile_number: str
    code: str = Field(min_length=4, max_length=8)
    language: Language = Language.ENGLISH

    @field_validator("mobile_number")
    @classmethod
    def _normalize(cls, value: str) -> str:
        return normalize_mobile(value)

    @field_validator("code")
    @classmethod
    def _digits(cls, value: str) -> str:
        return value.strip()


class DemoLoginIn(ApiModel):
    """Signs in as one of the seeded fictional demo patients."""

    demo_key: str = Field(min_length=1, max_length=40)


class SessionOut(ApiModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    patient: PatientOut
    onboarding: OnboardingProgressOut
    # True only on the request that created the patient record.
    is_new_patient: bool


class DemoPatientOut(ApiModel):
    demo_key: str
    label: Localised
    description: Localised
    mobile_number: str
