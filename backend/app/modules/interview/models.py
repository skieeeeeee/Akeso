"""Interview persistence.

The session stores NAVIGATION state only; clinical facts are written to
`medical_profiles` so there is exactly one source of truth for them. Answers
are also kept verbatim here as an audit trail (what was asked, what the
patient said, and how they said it).
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
from app.shared.enums import ConversationStatus, InputMethod

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.patient.models import Patient


class ConversationSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "conversation_sessions"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    encounter_id: Mapped[uuid.UUID | None] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("encounters.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[ConversationStatus] = mapped_column(
        enum_column(ConversationStatus, "conversation_status"),
        nullable=False,
        default=ConversationStatus.IN_PROGRESS,
        server_default=ConversationStatus.IN_PROGRESS.value,
        index=True,
    )
    current_section: Mapped[str] = mapped_column(sa.String(40), nullable=False, default="presenting")
    current_question_id: Mapped[str | None] = mapped_column(sa.String(80), nullable=True)
    progress_percent: Mapped[int] = mapped_column(sa.Integer(), nullable=False, default=0)

    # The serialised InterviewState — the engine owns its shape.
    state: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )
    # Set when the AI assist layer was unavailable, so the UI can say so.
    ai_fallback_active: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    patient: Mapped["Patient"] = relationship()
    answers: Mapped[list["ConversationAnswer"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ConversationAnswer.created_at",
    )


class ConversationAnswer(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One question/answer exchange, kept verbatim for audit."""

    __tablename__ = "conversation_answers"

    session_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("conversation_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[str] = mapped_column(sa.String(120), nullable=False)
    question_text: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    section: Mapped[str] = mapped_column(sa.String(40), nullable=False)
    # Exactly what the patient said or typed.
    raw_answer: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    # What the engine made of it.
    normalized_answer: Mapped[str] = mapped_column(sa.Text(), nullable=False, default="")
    input_method: Mapped[InputMethod] = mapped_column(
        enum_column(InputMethod, "input_method"),
        nullable=False,
        default=InputMethod.TEXT,
        server_default=InputMethod.TEXT.value,
    )
    # Clinical items derived from this answer, as written to the profile.
    extracted_items: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=sa.text("'[]'::jsonb")
    )
    # True when an AI reading of the answer was used, false for rule-based.
    ai_assisted: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )

    session: Mapped["ConversationSession"] = relationship(back_populates="answers")
