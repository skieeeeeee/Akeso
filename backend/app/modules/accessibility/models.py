"""Accessibility assessment responses and the resulting active preferences."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import enum_column
from app.shared.enums import (
    ContrastMode,
    DifficultyLevel,
    DigitalComfort,
    FontSize,
    InteractionPreference,
    InterfaceMode,
    Language,
    PreferenceSource,
    PreferredInteraction,
)

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.patient.models import Patient


class AccessibilityAssessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One completed assessment. Kept as history — a patient may retake it."""

    __tablename__ = "accessibility_assessments"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    digital_comfort: Mapped[DigitalComfort] = mapped_column(
        enum_column(DigitalComfort, "digital_comfort"), nullable=False
    )
    preferred_interaction: Mapped[PreferredInteraction] = mapped_column(
        enum_column(PreferredInteraction, "preferred_interaction"), nullable=False
    )
    reading_difficulty: Mapped[DifficultyLevel] = mapped_column(
        enum_column(DifficultyLevel, "difficulty_level"), nullable=False
    )
    hearing_difficulty: Mapped[DifficultyLevel] = mapped_column(
        enum_column(DifficultyLevel, "difficulty_level"), nullable=False
    )
    vision_difficulty: Mapped[DifficultyLevel] = mapped_column(
        enum_column(DifficultyLevel, "difficulty_level"), nullable=False
    )

    # Voluntary disclosures only — a list of AccessibilityNeed values.
    additional_needs: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=sa.text("'[]'::jsonb")
    )
    additional_notes: Mapped[str | None] = mapped_column(sa.Text(), nullable=True)

    # Snapshot of what the engine recommended from these answers, so a later
    # rule change never rewrites history.
    recommendation: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )
    # Age at assessment time; recorded because age influences the result and
    # date_of_birth may be edited afterwards.
    age_at_assessment: Mapped[int | None] = mapped_column(sa.Integer(), nullable=True)

    patient: Mapped["Patient"] = relationship(back_populates="assessments")


class PatientPreferences(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """The patient's ACTIVE experience settings.

    Always changeable — the patient is never locked into a mode.
    """

    __tablename__ = "patient_preferences"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    interface_mode: Mapped[InterfaceMode] = mapped_column(
        enum_column(InterfaceMode, "interface_mode"),
        nullable=False,
        default=InterfaceMode.STANDARD,
        server_default=InterfaceMode.STANDARD.value,
    )
    font_size: Mapped[FontSize] = mapped_column(
        enum_column(FontSize, "font_size"),
        nullable=False,
        default=FontSize.NORMAL,
        server_default=FontSize.NORMAL.value,
    )
    contrast_mode: Mapped[ContrastMode] = mapped_column(
        enum_column(ContrastMode, "contrast_mode"),
        nullable=False,
        default=ContrastMode.NORMAL,
        server_default=ContrastMode.NORMAL.value,
    )
    audio_guidance: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )
    interaction_preference: Mapped[InteractionPreference] = mapped_column(
        enum_column(InteractionPreference, "interaction_preference"),
        nullable=False,
        default=InteractionPreference.TOUCH,
        server_default=InteractionPreference.TOUCH.value,
    )
    language: Mapped[Language] = mapped_column(
        enum_column(Language, "language"),
        nullable=False,
        default=Language.ENGLISH,
        server_default=Language.ENGLISH.value,
    )
    source: Mapped[PreferenceSource] = mapped_column(
        enum_column(PreferenceSource, "preference_source"),
        nullable=False,
        default=PreferenceSource.RECOMMENDED,
        server_default=PreferenceSource.RECOMMENDED.value,
    )

    patient: Mapped["Patient"] = relationship(back_populates="preferences")
