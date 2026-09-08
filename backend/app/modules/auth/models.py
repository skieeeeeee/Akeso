"""Mocked OTP challenges.

The prototype has no SMS gateway. A real 6-digit code is generated and only
its hash is stored, so the verification path is the same shape a production
implementation would use — swapping in a gateway means changing the delivery
call, not the flow.
"""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class OtpChallenge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "otp_challenges"

    mobile_number: Mapped[str] = mapped_column(
        sa.String(20), nullable=False, index=True
    )
    code_hash: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    consumed_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )
    attempts: Mapped[int] = mapped_column(
        sa.Integer(), nullable=False, default=0, server_default="0"
    )
