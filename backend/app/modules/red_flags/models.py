"""Red-flag records.

One row per flag raised on an encounter. Rows are append-only from the
patient's side: nothing in the patient-facing API deletes or downgrades them.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.database.types import enum_column
from app.shared.enums import RedFlagCategory, RedFlagSource

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.encounter.models import Encounter


class RedFlag(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "red_flags"

    encounter_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("encounters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[RedFlagCategory] = mapped_column(
        enum_column(RedFlagCategory, "red_flag_category"), nullable=False, index=True
    )
    source: Mapped[RedFlagSource] = mapped_column(
        enum_column(RedFlagSource, "red_flag_source"),
        nullable=False,
        default=RedFlagSource.RULES,
        server_default=RedFlagSource.RULES.value,
    )
    # The patient's own words that caused this. Safe to show a clinician; the
    # matching criterion itself is never stored or returned.
    evidence: Mapped[str] = mapped_column(sa.String(300), nullable=False)
    # Set when a clinician reviews it in a later phase. A patient cannot.
    cleared_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    cleared_by: Mapped[str | None] = mapped_column(sa.String(120), nullable=True)

    encounter: Mapped["Encounter"] = relationship(back_populates="red_flags")
