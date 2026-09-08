"""Medical profile use cases."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.medical_history.models import (
    MEDICAL_PROFILE_SECTIONS,
    MedicalProfile,
)
from app.modules.medical_history.schemas import MedicalProfileIn
from app.modules.patient import service as patient_service
from app.modules.patient.models import Patient
from app.shared.clinical import ClinicalItem, dump_items, parse_items
from app.shared.enums import ClinicalSource, OnboardingStatus


def ensure_profile(db: Session, patient: Patient) -> MedicalProfile:
    if patient.medical_profile is None:
        patient.medical_profile = MedicalProfile(patient_id=patient.id)
        db.add(patient.medical_profile)
        db.flush()
    return patient.medical_profile


def read_sections(profile: MedicalProfile) -> dict[str, list[ClinicalItem]]:
    return {name: parse_items(profile.section(name)) for name in MEDICAL_PROFILE_SECTIONS}


def update(db: Session, patient: Patient, payload: MedicalProfileIn) -> MedicalProfile:
    """Replace the supplied sections.

    Everything written here is `source=PATIENT` with full confidence — it is
    what the patient said about themselves. Phase 2's document extraction
    writes into the same sections with `source=DOCUMENT` and a confidence
    score, which is why every item carries provenance.
    """
    profile = ensure_profile(db, patient)

    for section_name, items in payload.sections.items():
        clinical = [
            ClinicalItem(
                value=item.value,
                attributes=item.attributes,
                note=item.note,
                source=ClinicalSource.PATIENT,
                confidence=1.0,
                verified=False,
            )
            for item in items
            if item.value
        ]
        setattr(profile, section_name, dump_items(clinical))

    patient_service.mark_step_complete(
        db, patient, OnboardingStatus.MEDICAL_PROFILE_PENDING
    )
    db.flush()
    return profile
