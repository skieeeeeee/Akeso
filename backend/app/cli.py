"""Developer commands: `python -m app.cli <command>`.

Seeding runs through the real service layer rather than raw inserts, so the
demo data is produced by exactly the code the API uses — if a rule changes,
the seed changes with it.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import SessionLocal

# Registers every model on the shared Base before mappers configure.
from app.database import metadata as _metadata  # noqa: F401
from app.modules.abha import service as abha_service
from app.modules.accessibility import service as accessibility_service
from app.modules.accessibility.schemas import AssessmentIn
from app.modules.auth.models import OtpChallenge
from app.modules.consent import service as consent_service
from app.modules.consent.schemas import ConsentDecisionIn, ConsentSubmitIn
from app.modules.documents import pipeline
from app.modules.documents import service as document_service
from app.modules.documents.models import Document
from app.modules.encounter.models import Encounter
from app.modules.medical_history import service as medical_service
from app.modules.medical_history.schemas import MedicalItemIn, MedicalProfileIn
from app.modules.patient.demo import DEMO_PATIENTS, DemoPatientDefinition
from app.modules.patient.models import Patient
from app.shared.enums import (
    ConsentPurpose,
    DocumentType,
    EncounterPriority,
    EncounterStatus,
    OnboardingStatus,
    RedFlagStatus,
    VisitType,
)

RESERVED_ATTRS = {"note"}


def _medical_payload(definition: DemoPatientDefinition) -> MedicalProfileIn:
    sections: dict[str, list[MedicalItemIn]] = {}
    for section, entries in definition.medical.items():
        sections[section] = [
            MedicalItemIn(
                value=entry["value"],
                note=entry.get("note"),
                attributes={
                    key: value
                    for key, value in entry.items()
                    if key not in {"value"} | RESERVED_ATTRS
                },
            )
            for entry in entries
        ]
    return MedicalProfileIn(sections=sections)


def _seed_patient(db: Session, definition: DemoPatientDefinition) -> Patient:
    patient = db.scalar(
        select(Patient).where(Patient.mobile_number == definition.mobile_number)
    )
    if patient is None:
        patient = Patient(mobile_number=definition.mobile_number)
        db.add(patient)

    # --- personal information ---------------------------------------------
    patient.full_name = definition.full_name
    patient.date_of_birth = definition.date_of_birth
    patient.gender = definition.gender
    patient.preferred_language = definition.language
    patient.is_demo = True
    patient.onboarding_status = OnboardingStatus.ABHA_PENDING
    if definition.emergency_contact:
        name, number, relation = definition.emergency_contact
        patient.emergency_contact_name = name
        patient.emergency_contact_number = number
        patient.emergency_contact_relation = relation
    db.flush()

    # --- health ID ---------------------------------------------------------
    if definition.abha_id:
        abha_service.link(db, patient, definition.abha_id)
    elif definition.onboarding_status != OnboardingStatus.ABHA_PENDING:
        abha_service.skip(db, patient)

    # Personal info is complete, so move past that step.
    from app.modules.patient import service as patient_service

    patient_service.mark_step_complete(
        db, patient, OnboardingStatus.PERSONAL_INFO_PENDING
    )

    # --- accessibility assessment + preferences ---------------------------
    if definition.assessment is not None:
        a = definition.assessment
        accessibility_service.submit_assessment(
            db,
            patient,
            AssessmentIn(
                digital_comfort=a.digital_comfort,
                preferred_interaction=a.preferred_interaction,
                reading_difficulty=a.reading_difficulty,
                hearing_difficulty=a.hearing_difficulty,
                vision_difficulty=a.vision_difficulty,
                additional_needs=list(a.additional_needs),
            ),
        )
        # Accepting the recommendation is what a patient does on that screen.
        from app.modules.accessibility.schemas import PreferencesIn

        accessibility_service.update_preferences(
            db, patient, PreferencesIn(accepted_recommendation=True)
        )

    # --- consent -----------------------------------------------------------
    if definition.consents:
        consent_service.submit(
            db,
            patient,
            ConsentSubmitIn(
                decisions=[
                    ConsentDecisionIn(purpose=purpose, granted=True)
                    for purpose in definition.consents
                ]
                + [
                    ConsentDecisionIn(purpose=ConsentPurpose.ABHA_LINKAGE, granted=False)
                    for _ in ()
                ],
                language=definition.language,
            ),
        )

    # --- medical profile ---------------------------------------------------
    if definition.medical:
        medical_service.update(db, patient, _medical_payload(definition))

    # A patient who stopped part-way keeps the stage the definition names.
    patient.onboarding_status = definition.onboarding_status
    db.flush()
    return patient


def _seed_visits(db: Session, patient: Patient, definition: DemoPatientDefinition) -> None:
    """Submitted past visits — what makes a patient "returning"."""
    if not definition.visits:
        return
    existing = db.scalar(select(Encounter).where(Encounter.patient_id == patient.id))
    if existing is not None:
        return

    for index, visit in enumerate(sorted(definition.visits, key=lambda v: -v.days_ago)):
        started = datetime.now(UTC) - timedelta(days=visit.days_ago)
        db.add(
            Encounter(
                patient_id=patient.id,
                status=EncounterStatus.COMPLETED,
                visit_type=VisitType.FIRST_VISIT if index == 0 else VisitType.FOLLOW_UP,
                priority=(
                    EncounterPriority.URGENT if visit.was_urgent else EncounterPriority.ROUTINE
                ),
                red_flag_status=(
                    RedFlagStatus.ACTIVE if visit.was_urgent else RedFlagStatus.NONE
                ),
                chief_complaint=visit.complaint,
                structured_history=(
                    {
                        "chief_complaint": [
                            {"value": visit.complaint, "source": "patient", "confidence": 1.0}
                        ],
                        "history_of_present_illness": (
                            [{"value": visit.detail, "source": "patient", "confidence": 1.0}]
                            if visit.detail
                            else []
                        ),
                    }
                ),
                patient_confirmed=True,
                started_at=started,
                completed_at=started + timedelta(minutes=28),
                submitted_at=started + timedelta(minutes=30),
            )
        )
    db.flush()


def _seed_documents(db: Session, patient: Patient, definition: DemoPatientDefinition) -> None:
    """Upload and actually process the demo records.

    Runs the real upload + OCR + extraction pipeline rather than inserting
    rows, so the timeline, findings and lab flags in the demo are produced by
    the same code the app uses.
    """
    if not definition.documents:
        return
    if db.scalar(select(Document).where(Document.patient_id == patient.id)):
        return

    for entry in definition.documents:
        document = document_service.upload(
            db,
            patient,
            file_name=f"{entry.title.lower().replace(' ', '_')}.txt",
            mime_type="text/plain",
            content=entry.text.encode(),
            document_type=DocumentType(entry.document_type),
            title=entry.title,
        )
        # Synchronous entry point for the async pipeline.
        asyncio.run(pipeline.process(db, document))
    db.flush()


def seed() -> None:
    with SessionLocal() as db:
        for definition in DEMO_PATIENTS.values():
            patient = _seed_patient(db, definition)
            _seed_visits(db, patient, definition)
            _seed_documents(db, patient, definition)
            findings = sum(len(d.extracted_items) for d in patient.documents)
            print(
                f"  {definition.demo_key:12} {definition.full_name:14} "
                f"age {patient.age:<4} {patient.onboarding_status.value:24} "
                f"{len(definition.visits)} visit(s) {len(patient.documents)} doc(s) "
                f"{findings} finding(s)"
            )
        db.commit()
    print("\nDemo data ready. All medical information is fictional.")


def reset() -> None:
    """Remove demo patients and expired OTP challenges."""
    with SessionLocal() as db:
        patients = db.scalars(select(Patient).where(Patient.is_demo.is_(True))).all()
        for patient in patients:
            db.delete(patient)
        db.execute(delete(OtpChallenge))
        db.commit()
        print(f"Removed {len(patients)} demo patient(s) and all OTP challenges.")


def status() -> None:
    with SessionLocal() as db:
        total = db.scalar(select(Patient).with_only_columns(Patient.id).exists().select())
        patients = db.scalars(select(Patient)).all()
        print(f"patients: {len(patients)} (any: {total})")
        for patient in patients:
            prefs = patient.preferences
            print(
                f"  {patient.mobile_number}  {patient.display_name:16} "
                f"{patient.onboarding_status.value:24} "
                f"{'demo' if patient.is_demo else 'live':5} "
                f"{(prefs.interface_mode.value + '/' + prefs.font_size.value) if prefs else '-'}"
            )


COMMANDS = {"seed": seed, "reset": reset, "status": status}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: python -m app.cli [{' | '.join(COMMANDS)}]")
        return 1
    COMMANDS[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
