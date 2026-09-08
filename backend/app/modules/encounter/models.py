"""Visits.

Created in Phase 1 because the returning-patient journey and the doctor
workflow both hang off it. Phase 1 only ever creates the encounter row that
represents onboarding completion; the interview lives in Phase 2.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import enum_column
from app.shared.enums import (
    CareSystem,
    EncounterPriority,
    EncounterStatus,
    RedFlagStatus,
    VisitType,
)

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.documents.models import Document
    from app.modules.patient.models import Patient
    from app.modules.red_flags.models import RedFlag


class Encounter(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "encounters"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[EncounterStatus] = mapped_column(
        enum_column(EncounterStatus, "encounter_status"),
        nullable=False,
        default=EncounterStatus.DRAFT,
        server_default=EncounterStatus.DRAFT.value,
        index=True,
    )
    priority: Mapped[EncounterPriority] = mapped_column(
        enum_column(EncounterPriority, "encounter_priority"),
        nullable=False,
        default=EncounterPriority.ROUTINE,
        server_default=EncounterPriority.ROUTINE.value,
    )
    visit_type: Mapped[VisitType] = mapped_column(
        enum_column(VisitType, "visit_type"),
        nullable=False,
        default=VisitType.FIRST_VISIT,
        server_default=VisitType.FIRST_VISIT.value,
    )

    # Which system of medicine this visit is for. Set from the first question
    # and it decides how long the interview is.
    care_system: Mapped[CareSystem | None] = mapped_column(
        enum_column(CareSystem, "care_system"), nullable=True, index=True
    )

    chief_complaint: Mapped[str | None] = mapped_column(sa.Text(), nullable=True)
    # Phase 2 writes the interview transcript and structured findings here.
    structured_history: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )

    # --- Safety -----------------------------------------------------------
    # Raised by screening; a patient-facing endpoint can never lower it.
    red_flag_status: Mapped[RedFlagStatus] = mapped_column(
        enum_column(RedFlagStatus, "red_flag_status"),
        nullable=False,
        default=RedFlagStatus.NONE,
        server_default=RedFlagStatus.NONE.value,
        index=True,
    )
    red_flag_acknowledged_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    # Set when the patient asks for help from the emergency screen.
    assistance_requested_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    # --- Submission -------------------------------------------------------
    submitted_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    # Confirmed by the patient on the review screen before submission.
    patient_confirmed: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )

    started_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    patient: Mapped["Patient"] = relationship(back_populates="encounters")
    documents: Mapped[list["Document"]] = relationship(back_populates="encounter")
    red_flags: Mapped[list["RedFlag"]] = relationship(
        back_populates="encounter", cascade="all, delete-orphan"
    )

    @property
    def is_submitted(self) -> bool:
        return self.submitted_at is not None

    def complaint_or_none(self) -> str | None:
        """Trimmed chief complaint, or None when nothing was recorded."""
        return (self.chief_complaint or "").strip() or None
