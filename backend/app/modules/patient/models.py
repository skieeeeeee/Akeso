"""Patient identity — the root of every relationship in the schema."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import enum_column
from app.shared.enums import CareSystem, Gender, Language, OnboardingStatus

if TYPE_CHECKING:  # pragma: no cover - typing only
    from app.modules.abha.models import AbhaProfile
    from app.modules.accessibility.models import (
        AccessibilityAssessment,
        PatientPreferences,
    )
    from app.modules.consent.models import Consent
    from app.modules.documents.models import Document
    from app.modules.encounter.models import Encounter
    from app.modules.medical_history.models import MedicalProfile


class Patient(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "patients"

    # Nullable by design: the patient authenticates with a mobile number
    # before the personal-information step collects their name.
    full_name: Mapped[str | None] = mapped_column(sa.String(160), nullable=True)
    mobile_number: Mapped[str] = mapped_column(
        sa.String(20), nullable=False, unique=True, index=True
    )
    # Age is DERIVED from this column (see `age`), never stored separately.
    date_of_birth: Mapped[date | None] = mapped_column(sa.Date(), nullable=True)
    gender: Mapped[Gender | None] = mapped_column(
        enum_column(Gender, "gender"), nullable=True
    )
    preferred_language: Mapped[Language] = mapped_column(
        enum_column(Language, "language"),
        nullable=False,
        default=Language.ENGLISH,
        server_default=Language.ENGLISH.value,
    )

    emergency_contact_name: Mapped[str | None] = mapped_column(
        sa.String(160), nullable=True
    )
    emergency_contact_number: Mapped[str | None] = mapped_column(
        sa.String(20), nullable=True
    )
    emergency_contact_relation: Mapped[str | None] = mapped_column(
        sa.String(60), nullable=True
    )

    # The system the patient chose last time, pre-selected on the next visit
    # so a returning patient is not asked cold.
    preferred_care_system: Mapped[CareSystem | None] = mapped_column(
        enum_column(CareSystem, "care_system"), nullable=True
    )

    onboarding_status: Mapped[OnboardingStatus] = mapped_column(
        enum_column(OnboardingStatus, "onboarding_status"),
        nullable=False,
        default=OnboardingStatus.ABHA_PENDING,
        server_default=OnboardingStatus.ABHA_PENDING.value,
        index=True,
    )
    # Marks the fictional records used for demonstration.
    is_demo: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )

    # --- Relationships -----------------------------------------------------
    abha_profile: Mapped["AbhaProfile | None"] = relationship(
        back_populates="patient", uselist=False, cascade="all, delete-orphan"
    )
    preferences: Mapped["PatientPreferences | None"] = relationship(
        back_populates="patient", uselist=False, cascade="all, delete-orphan"
    )
    assessments: Mapped[list["AccessibilityAssessment"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="AccessibilityAssessment.created_at.desc()",
    )
    consents: Mapped[list["Consent"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="Consent.created_at.desc()",
    )
    medical_profile: Mapped["MedicalProfile | None"] = relationship(
        back_populates="patient", uselist=False, cascade="all, delete-orphan"
    )
    encounters: Mapped[list["Encounter"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="Encounter.created_at.desc()",
    )
    documents: Mapped[list["Document"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="Document.created_at.desc()",
    )

    @property
    def age(self) -> int | None:
        """Age in whole years, derived from `date_of_birth`."""
        if self.date_of_birth is None:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return max(0, years)

    @property
    def display_name(self) -> str:
        return self.full_name or "New patient"

    @property
    def onboarding_complete(self) -> bool:
        return self.onboarding_status == OnboardingStatus.COMPLETED

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Patient {self.display_name!r} {self.mobile_number}>"
