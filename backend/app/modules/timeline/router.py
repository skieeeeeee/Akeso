"""Timeline endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.patient.models import Patient
from app.modules.timeline import service
from app.shared.enums import TimelineEventType
from app.shared.schemas import ApiModel

router = APIRouter(prefix="/timeline", tags=["timeline"])

DISCLAIMER = {
    "en": "This is a record of what you told us and what your documents say. "
    "It is not a diagnosis — your doctor will review it with you.",
    "hi": "यह उसका रिकॉर्ड है जो आपने बताया और जो आपके दस्तावेज़ों में लिखा है। "
    "यह निदान नहीं है — आपके डॉक्टर इसे आपके साथ देखेंगे।",
}


class TimelineOut(ApiModel):
    events: list[dict]
    total: int
    # Counts per event type, so the UI can offer filters that are never empty.
    counts: dict[str, int]
    disclaimer: dict[str, str]


@router.get("", response_model=TimelineOut)
def read_timeline(
    event_type: list[TimelineEventType] | None = Query(default=None),
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> TimelineOut:
    """The patient's chronological record, newest first."""
    events = service.build(db, patient)

    counts: dict[str, int] = {}
    for event in events:
        counts[event.event_type.value] = counts.get(event.event_type.value, 0) + 1

    if event_type:
        wanted = {value.value for value in event_type}
        events = [event for event in events if event.event_type.value in wanted]

    return TimelineOut(
        events=[event.as_dict() for event in events],
        total=len(events),
        counts=counts,
        disclaimer=DISCLAIMER,
    )
