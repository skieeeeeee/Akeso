"""ABHA linkage.

MOCK ONLY: no ABDM network call exists anywhere in this codebase. The table
keeps the shape a real integration would need (`is_mock`, `verification_status`,
`failure_reason`) so switching to ABDM later is an adapter change, not a
schema migration.
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
from app.shared.enums import AbhaVerificationStatus

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.patient.models import Patient


class AbhaProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "abha_profiles"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    abha_id: Mapped[str | None] = mapped_column(sa.String(64), nullable=True, index=True)
    verification_status: Mapped[AbhaVerificationStatus] = mapped_column(
        enum_column(AbhaVerificationStatus, "abha_verification_status"),
        nullable=False,
        default=AbhaVerificationStatus.UNVERIFIED,
        server_default=AbhaVerificationStatus.UNVERIFIED.value,
    )
    linked_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    # Human-readable reason a link attempt did not succeed, shown in the UI.
    failure_reason: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    is_mock: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=True, server_default=sa.true()
    )

    patient: Mapped["Patient"] = relationship(back_populates="abha_profile")
