"""Consent records.

Granular by `purpose` and revocable, so ABDM-style consent artefacts can be
layered on later without changing the table.
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
from app.shared.enums import ConsentPurpose, ConsentStatus

if TYPE_CHECKING:  # pragma: no cover
    from app.modules.patient.models import Patient


class Consent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "consents"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    purpose: Mapped[ConsentPurpose] = mapped_column(
        enum_column(ConsentPurpose, "consent_purpose"), nullable=False, index=True
    )
    status: Mapped[ConsentStatus] = mapped_column(
        enum_column(ConsentStatus, "consent_status"), nullable=False
    )
    # Version of the consent text the patient actually saw.
    text_version: Mapped[str] = mapped_column(
        sa.String(32), nullable=False, default="2026-01", server_default="2026-01"
    )
    language: Mapped[str] = mapped_column(sa.String(8), nullable=False, default="en")

    granted_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    declined_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    patient: Mapped["Patient"] = relationship(back_populates="consents")

    @property
    def is_active(self) -> bool:
        return self.status == ConsentStatus.GRANTED and self.revoked_at is None
