"""Chronological medical timeline.

Assembled by reading what other features already store — documents, their
extracted findings, and past encounters. It owns no data of its own, so it can
never disagree with the records it summarises.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.documents.models import Document, ExtractedMedicalData
from app.modules.encounter.models import Encounter
from app.modules.patient.models import Patient
from app.shared.i18n import localise, t
from app.shared.enums import (
    ExtractedEntityType,
    LabFlag,
    ReviewState,
    TimelineEventType,
)

# Which extracted entity types earn their own timeline entry. Notes and vitals
# are excluded — they would bury the clinically useful events.
_HOSPITAL_VISIT = t("Hospital visit", "अस्पताल की मुलाक़ात")

ENTITY_EVENT_TYPES: dict[ExtractedEntityType, TimelineEventType] = {
    ExtractedEntityType.DIAGNOSIS: TimelineEventType.DIAGNOSIS,
    ExtractedEntityType.MEDICATION: TimelineEventType.MEDICATION,
    ExtractedEntityType.INVESTIGATION: TimelineEventType.INVESTIGATION,
    ExtractedEntityType.SURGERY: TimelineEventType.SURGERY,
    ExtractedEntityType.PROCEDURE: TimelineEventType.SURGERY,
}


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    id: str
    event_type: TimelineEventType
    event_date: date | None
    title: str
    detail: str
    # An enum the client labels itself, when the detail is a status or a kind
    # rather than words quoted from a document.
    detail_kind: str
    # Where this came from, so the UI never presents a finding as a fact.
    # Structured rather than a pre-built English sentence, so the client can
    # compose it in the patient's language.
    source_kind: str
    source_name: str
    document_id: str | None
    # Only set for investigations with a printed reference range.
    flag: LabFlag | None
    requires_review: bool

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "title": self.title,
            "detail": self.detail,
            "detail_kind": self.detail_kind,
            "source_kind": self.source_kind,
            "source_name": self.source_name,
            "document_id": self.document_id,
            "flag": self.flag.value if self.flag else None,
            "requires_review": self.requires_review,
        }


def _describe(item: ExtractedMedicalData) -> str:
    if item.entity_type == ExtractedEntityType.INVESTIGATION:
        parts = [item.numeric_value or "", item.unit or ""]
        if item.reference_range:
            parts.append(f"(reference {item.reference_range})")
        return " ".join(part for part in parts if part).strip()
    bits = [item.attributes.get(key, "") for key in ("dose", "frequency", "duration")]
    return " · ".join(bit for bit in bits if bit)


def build(db: Session, patient: Patient) -> list[TimelineEvent]:
    """Every dated event we know about, newest first."""
    documents = list(
        db.scalars(
            select(Document)
            .where(Document.patient_id == patient.id)
            .options(selectinload(Document.extracted_items))
            .order_by(Document.created_at.desc())
        ).all()
    )
    encounters = list(
        db.scalars(select(Encounter).where(Encounter.patient_id == patient.id)).all()
    )

    events: list[TimelineEvent] = []

    for document in documents:
        label = (document.title or document.file_name).strip()
        events.append(
            TimelineEvent(
                id=f"doc:{document.id}",
                event_type=TimelineEventType.DOCUMENT,
                event_date=document.document_date or document.created_at.date(),
                title=label,
                detail="",
                detail_kind=document.document_type.value,
                source_kind="uploaded_document",
                source_name=label,
                document_id=str(document.id),
                flag=None,
                requires_review=document.processing_status.value
                in ("failed", "needs_review"),
            )
        )
        for item in document.extracted_items:
            event_type = ENTITY_EVENT_TYPES.get(item.entity_type)
            if event_type is None or item.review_state == ReviewState.REJECTED:
                continue
            events.append(
                TimelineEvent(
                    id=f"item:{item.id}",
                    event_type=event_type,
                    event_date=item.event_date or document.document_date,
                    title=item.value,
                    detail=_describe(item),
                    detail_kind="",
                    source_kind="found_in_document",
                    source_name=label,
                    document_id=str(document.id),
                    flag=item.flag,
                    requires_review=item.review_state == ReviewState.UNREVIEWED,
                )
            )

    for encounter in encounters:
        when = encounter.completed_at or encounter.started_at or encounter.created_at
        events.append(
            TimelineEvent(
                id=f"enc:{encounter.id}",
                event_type=TimelineEventType.VISIT,
                event_date=when.date() if when else None,
                title=encounter.chief_complaint
                or localise(_HOSPITAL_VISIT, patient.preferred_language),
                detail="",
                detail_kind=encounter.status.value,
                source_kind="visit_record",
                source_name="",
                document_id=None,
                flag=None,
                requires_review=False,
            )
        )

    # Undated events sort last rather than being dropped.
    events.sort(
        key=lambda event: (event.event_date is not None, event.event_date or date.min),
        reverse=True,
    )
    return events
