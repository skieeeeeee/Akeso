"""Medical profile endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.medical_history import service, structured
from app.modules.medical_history.content import MEDICAL_SECTIONS
from app.shared.i18n import Localised, t
from app.shared.schemas import ApiModel
from app.modules.medical_history.schemas import (
    MedicalContentOut,
    MedicalProfileIn,
    MedicalProfileOut,
)
from app.modules.patient import service as patient_service

from app.modules.patient.models import Patient

router = APIRouter(prefix="/patients/me/medical-profile", tags=["medical-history"])


def _out(patient: Patient, profile) -> MedicalProfileOut:
    sections = service.read_sections(profile)
    progress = patient_service.progress(patient)
    return MedicalProfileOut(
        sections=sections,
        total_items=sum(len(items) for items in sections.values()),
        updated_at=profile.updated_at,
        onboarding_status=str(progress["status"]),
        next_route=str(progress["next_route"]),
    )


@router.get("/content", response_model=MedicalContentOut)
def get_content() -> MedicalContentOut:
    """Section titles, prompts and quick-pick suggestions, in every language."""
    return MedicalContentOut(sections=MEDICAL_SECTIONS)


@router.get("", response_model=MedicalProfileOut)
def get_profile(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> MedicalProfileOut:
    return _out(patient, service.ensure_profile(db, patient))


@router.put("", response_model=MedicalProfileOut)
def put_profile(
    payload: MedicalProfileIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> MedicalProfileOut:
    """Save the health history. Sections not supplied are left unchanged."""
    return _out(patient, service.update(db, patient, payload))



class StructuredHistoryOut(ApiModel):
    """The generated history, with every fact labelled by where it came from."""

    sections: dict[str, list[dict[str, Any]]]
    labels: dict[str, str]
    patient_reported_count: int
    document_derived_count: int
    # Sections a doctor would expect to see and that are still empty.
    missing_sections: list[str]
    ayush_included: bool
    narrative: str
    # "template" (deterministic) or "ai".
    narrative_source: str
    disclaimer: dict[str, str]


DISCLAIMER: Localised = t(
    "This summarises what you told us and what your documents say. "
    "It is not a diagnosis, and your doctor will go through it with you.",
    "यह उसका सारांश है जो आपने बताया और जो आपके दस्तावेज़ों में लिखा है। "
    "यह निदान नहीं है, और आपके डॉक्टर इसे आपके साथ देखेंगे।",
)


@router.get("/structured", response_model=StructuredHistoryOut)
async def read_structured(
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> StructuredHistoryOut:
    """The review view: patient-reported and document-derived, side by side."""
    history = structured.build(db, patient)
    text, source = await structured.narrative(db, patient, history)
    # Section names and stored sentinels come back in the patient's language.
    history["labels"] = structured.section_labels(patient.preferred_language)
    history = structured.for_display(history, patient.preferred_language)
    return StructuredHistoryOut(
        **history, narrative=text, narrative_source=source, disclaimer=DISCLAIMER
    )
