"""The patient's standing medical profile.

This is the record that makes a returning visit short: it is built once during
onboarding and then amended, so a returning patient describes only new
symptoms instead of repeating their whole history.

Each clinical section is a JSONB list of provenance-carrying items (see
`app.shared.clinical.ClinicalItem`) rather than free text, so Phase 2's OCR
and AI extraction have a typed place to write, and every value can say where
it came from and whether a clinician verified it.
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

EMPTY_LIST = sa.text("'[]'::jsonb")

# The clinical sections stored on the profile. Declared once so the schema,
# the service layer and the UI all iterate the same list.
MEDICAL_PROFILE_SECTIONS: tuple[str, ...] = (
    # Phase 2 additions: the presenting problem and two review sections.
    "chief_complaint",
    "history_of_present_illness",
    "past_medical_history",
    "surgical_history",
    "current_medications",
    "drug_history",
    "allergies",
    "family_history",
    "personal_history",
    "previous_investigations",
    "review_of_systems",
    "additional_information",
)


def _section() -> Mapped[list[dict[str, Any]]]:
    return mapped_column(
        JSONB, nullable=False, default=list, server_default=EMPTY_LIST
    )


class MedicalProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "medical_profiles"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        PgUUID(as_uuid=True),
        sa.ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    chief_complaint: Mapped[list[dict[str, Any]]] = _section()
    history_of_present_illness: Mapped[list[dict[str, Any]]] = _section()
    past_medical_history: Mapped[list[dict[str, Any]]] = _section()
    surgical_history: Mapped[list[dict[str, Any]]] = _section()
    current_medications: Mapped[list[dict[str, Any]]] = _section()
    drug_history: Mapped[list[dict[str, Any]]] = _section()
    allergies: Mapped[list[dict[str, Any]]] = _section()
    family_history: Mapped[list[dict[str, Any]]] = _section()
    personal_history: Mapped[list[dict[str, Any]]] = _section()
    previous_investigations: Mapped[list[dict[str, Any]]] = _section()
    review_of_systems: Mapped[list[dict[str, Any]]] = _section()
    additional_information: Mapped[list[dict[str, Any]]] = _section()

    patient: Mapped["Patient"] = relationship(back_populates="medical_profile")

    def section(self, name: str) -> list[dict[str, Any]]:
        if name not in MEDICAL_PROFILE_SECTIONS:
            raise KeyError(f"Unknown medical profile section: {name}")
        return getattr(self, name)

    @property
    def recorded_item_count(self) -> int:
        return sum(len(self.section(name)) for name in MEDICAL_PROFILE_SECTIONS)
