"""The returning-patient home screen, assembled in one request.

Reads from the features that own each piece rather than storing anything of
its own, so the home screen can never show something the profile disagrees
with. Every list is capped — the brief is a useful screen, not a data dump.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.documents.models import Document
from app.modules.encounter.models import Encounter
from app.modules.medical_history import service as medical_service
from app.modules.patient.models import Patient
from app.modules.patient.onboarding import progress_for
from app.modules.timeline import service as timeline_service
from app.shared.i18n import Localised, t
from app.shared.enums import RedFlagStatus

NONE_REPORTED = "None reported"

GREETING: Localised = t("Welcome back", "आपका फिर से स्वागत है")
NEW_PATIENT_GREETING: Localised = t("Welcome", "स्वागत है")


def _values(items, limit: int) -> list[str]:
    return [item.value for item in items if item.value != NONE_REPORTED][:limit]


def build(db: Session, patient: Patient) -> dict[str, Any]:
    profile = medical_service.ensure_profile(db, patient)
    sections = medical_service.read_sections(profile)

    encounters = list(
        db.scalars(
            select(Encounter)
            .where(Encounter.patient_id == patient.id)
            .options(selectinload(Encounter.red_flags))
            .order_by(Encounter.created_at.desc())
            .limit(5)
        ).all()
    )
    submitted = [encounter for encounter in encounters if encounter.submitted_at]
    in_progress = next(
        (encounter for encounter in encounters if encounter.submitted_at is None), None
    )

    documents = list(
        db.scalars(
            select(Document)
            .where(Document.patient_id == patient.id)
            .order_by(Document.created_at.desc())
            .limit(3)
        ).all()
    )

    # The timeline is already an aggregation; take its head for the home card.
    try:
        recent_events = [event.as_dict() for event in timeline_service.build(db, patient)[:4]]
    except Exception:  # noqa: BLE001 - a home screen must still render
        recent_events = []

    onboarding = progress_for(patient.onboarding_status)
    total_items = sum(len(items) for items in sections.values())

    last = submitted[0] if submitted else None

    return {
        "patient": patient,
        "greeting": GREETING if submitted else NEW_PATIENT_GREETING,
        "onboarding": {
            "status": onboarding.status,
            "step_number": onboarding.step_number,
            "total_steps": onboarding.total_steps,
            "percent": onboarding.percent,
            "next_route": onboarding.next_route,
            "is_complete": onboarding.is_complete,
        },
        "profile_complete": onboarding.is_complete and total_items > 0,
        "history_item_count": total_items,
        # Short, high-value summaries only.
        "conditions": _values(sections["past_medical_history"], 4),
        "medications": _values(sections["current_medications"], 4),
        "allergies": _values(sections["allergies"], 4),
        "recent_documents": [
            {
                "id": str(document.id),
                "title": document.title or document.file_name,
                "type": document.document_type.value,
                "status": document.processing_status.value,
                "date": document.document_date.isoformat() if document.document_date else None,
            }
            for document in documents
        ],
        "document_count": len(documents),
        "recent_events": recent_events,
        "last_visit": (
            {
                "id": str(last.id),
                "complaint": last.complaint_or_none(),
                "submitted_at": last.submitted_at,
                "priority": last.priority.value,
                "was_urgent": last.red_flag_status == RedFlagStatus.ACTIVE,
            }
            if last
            else None
        ),
        "visit_count": len(submitted),
        # Set when a visit was started but never submitted, so the home screen
        # can offer to resume rather than silently starting a second one.
        "visit_in_progress": (
            {
                "id": str(in_progress.id),
                "complaint": in_progress.complaint_or_none(),
                "started_at": in_progress.started_at,
                "is_urgent": in_progress.red_flag_status == RedFlagStatus.ACTIVE,
            }
            if in_progress
            else None
        ),
    }


def last_interaction(encounters: list[Encounter]) -> datetime | None:
    dates = [encounter.submitted_at for encounter in encounters if encounter.submitted_at]
    return max(dates) if dates else None
