"""AYUSH (Ayurvedic) assessment.

Its own table because it is a distinct examination framework, not a subset of
the allopathic history — and because it is optional, so it must be absent
rather than half-filled for patients who do not opt in.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.patient.models import Patient


class AyushAssessment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ayush_assessments"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Dashavidha Pariksha: {pariksha_key: selected value}. JSONB because the
    # ten factors are independent observations and adding one should not need
    # a migration.
    dashavidha: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )
    # Ahara (diet) and Vihara (routine) as lists of selected values.
    ahara: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=sa.text("'[]'::jsonb")
    )
    vihara: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=sa.text("'[]'::jsonb")
    )
    # Ashtasthana Pariksha: the eight-fold examination.
    ashtasthana: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )
    # Agni/Koshtha, Nidra and Manas — digestion, sleep and mental state.
    lifestyle: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=sa.text("'{}'::jsonb")
    )
    notes: Mapped[str | None] = mapped_column(sa.Text(), nullable=True)
    is_complete: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )

    patient: Mapped["Patient"] = relationship()

    @property
    def answered_count(self) -> int:
        """How many examination factors carry an answer."""
        return (
            len([v for v in self.dashavidha.values() if v])
            + len([v for v in self.ashtasthana.values() if v])
            + len([v for v in self.lifestyle.values() if v])
            + len(self.ahara)
            + len(self.vihara)
        )
