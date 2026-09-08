"""Encounter (new visit) endpoints."""

from __future__ import annotations

import uuid

import jwt
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.encounter import service, summary
from app.modules.encounter.schemas import (
    ConfirmEncounterIn,
    EncounterAnswerIn,
    EncounterReviewOut,
    EncounterSummaryOut,
    EncounterView,
    StartVisitIn,
    TodayAnswer,
)
from app.modules.encounter import handoff
from app.modules.encounter.script import ENCOUNTER_SCRIPT
from app.modules.medical_history.structured import section_labels
from app.modules.patient.models import Patient
from app.modules.ayush import service as ayush_service
from app.modules.red_flags import service as red_flag_service
from app.shared.errors import AuthenticationError
from app.shared.i18n import Localised, t
from app.shared.enums import (
    AnswerKind,
    CareSystem,
    PARTIAL_AYUSH_SYSTEMS,
    RedFlagStatus,
)

# Any system whose visit opens an AYUSH section, so the review screen reports
# the extra questions the patient answered.
AYUSH_CARE_SYSTEMS = frozenset({CareSystem.AYURVEDA}) | PARTIAL_AYUSH_SYSTEMS

router = APIRouter(prefix="/encounters", tags=["encounter"])

SUBMITTED_MESSAGE: Localised = t(
    "Your visit details have been sent to the care team. Please wait to be called.",
    "आपकी मुलाक़ात की जानकारी देखभाल टीम को भेज दी गई है। कृपया बुलाए जाने तक प्रतीक्षा करें।",
)
SUBMITTED_URGENT: Localised = t(
    "Your visit has been sent and marked urgent. Please stay near the staff desk.",
    "आपकी जानकारी भेज दी गई है और अत्यावश्यक चिह्नित है। कृपया स्टाफ़ डेस्क के पास रहें।",
)


@router.post("/start", response_model=EncounterView)
def start_visit(
    payload: StartVisitIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    """Begin a new visit, or resume one already in progress."""
    encounter = service.start(db, patient, payload)
    return service.build_view(db, patient, encounter)


@router.get("/current", response_model=EncounterView | None)
def current_visit(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> EncounterView | None:
    encounter = service.active_encounter(db, patient)
    return service.build_view(db, patient, encounter) if encounter else None


@router.get("/{encounter_id}", response_model=EncounterView)
def read_visit(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    return service.build_view(db, patient, service.get(db, patient, encounter_id))


@router.post("/{encounter_id}/answer", response_model=EncounterView)
async def answer_visit(
    encounter_id: uuid.UUID,
    payload: EncounterAnswerIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    """Record one answer about today's concern and re-screen for red flags."""
    return await service.answer(db, patient, encounter_id, payload)


@router.post("/{encounter_id}/back", response_model=EncounterView)
def back_visit(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    return service.back(db, patient, encounter_id)


@router.get("/{encounter_id}/safety", response_model=None)
def read_safety(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
):
    """Current safety state. Never returns the criteria that raised a flag."""
    encounter = service.get(db, patient, encounter_id)
    return red_flag_service.state_for(db, encounter)


@router.post("/{encounter_id}/safety/acknowledge", response_model=EncounterView)
def acknowledge_safety(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    """Record that the patient saw the emergency screen and will continue.

    Note there is deliberately NO endpoint to clear a flag or lower priority:
    a patient cannot de-escalate their own visit.
    """
    encounter = service.acknowledge_safety(db, patient, encounter_id)
    return service.build_view(db, patient, encounter)


@router.post("/{encounter_id}/safety/assistance", response_model=EncounterView)
def request_assistance(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterView:
    """The patient is asking for immediate help."""
    encounter = service.request_assistance(db, patient, encounter_id)
    return service.build_view(db, patient, encounter)


@router.get("/{encounter_id}/review", response_model=EncounterReviewOut)
async def review_visit(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterReviewOut:
    """Everything the patient checks before submitting."""
    encounter = service.get(db, patient, encounter_id)
    existing = service.existing_context(db, patient, encounter)
    text, source = await summary.narrative(db, patient, encounter, existing)

    # A gate question ("have your medicines changed?") carries no clinical
    # value of its own, and a skipped question is noise on a review screen —
    # so neither is listed as an answer. The skipped count is reported
    # instead, so nothing is silently hidden.
    reported: list[TodayAnswer] = []
    skipped = 0
    severity: str | None = None
    for row in service.answers_for(db, encounter):
        question = ENCOUNTER_SCRIPT.question_by_id(row.question_id)
        answer = (row.normalized_answer or row.raw_answer or "").strip()
        if question is not None and question.target is None:
            continue  # navigation gate
        if not answer or answer == service.NONE_REPORTED:
            skipped += 1
            continue
        if question is not None and question.kind == AnswerKind.SCALE:
            severity = answer
            continue  # shown as a metric, not as a row
        reported.append(
            TodayAnswer(
                question_text=row.question_text,
                answer=answer,
                section=row.section,
                input_method=row.input_method,
            )
        )

    return EncounterReviewOut(
        encounter_id=encounter.id,
        chief_complaint=encounter.chief_complaint,
        today=service.today_sections(encounter),
        today_answers=reported,
        skipped_count=skipped,
        severity=severity,
        existing=existing,
        documents_today=[
            {
                "id": str(document.id),
                "title": document.title or document.file_name,
                "type": document.document_type.value,
                "status": document.processing_status.value,
            }
            for document in encounter.documents
        ],
        safety=red_flag_service.state_for(db, encounter),
        priority=encounter.priority,
        narrative=text,
        narrative_source=source,
        labels=section_labels(patient.preferred_language),
        ayush=ayush_service.recorded_for_review(
            ayush_service.get(db, patient), patient.preferred_language
        )
        if encounter.care_system in AYUSH_CARE_SYSTEMS
        else None,
        missing=summary.missing_today(encounter),
        disclaimer=summary.DISCLAIMER,
        submitted_at=encounter.submitted_at,
        patient_confirmed=encounter.patient_confirmed,
    )


@router.post("/{encounter_id}/submit", response_model=EncounterSummaryOut)
def submit_visit(
    encounter_id: uuid.UUID,
    payload: ConfirmEncounterIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> EncounterSummaryOut:
    """Submit the visit. Idempotent — a repeat call returns the same result."""
    encounter = service.confirm_and_submit(db, patient, encounter_id, payload)
    urgent = encounter.red_flag_status == RedFlagStatus.ACTIVE
    return EncounterSummaryOut(
        encounter_id=encounter.id,
        status=encounter.status,
        priority=encounter.priority,
        submitted_at=encounter.submitted_at,
        message=SUBMITTED_URGENT if urgent else SUBMITTED_MESSAGE,
    )


@router.get("/{encounter_id}/handoff")
def visit_handoff(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> dict:
    """The clinician-facing document that goes into the QR code.

    Exposed as JSON as well as an image so the patient can see exactly what
    they are about to show someone — a QR whose contents you cannot read is a
    poor thing to ask anyone to trust with their medical history.
    """
    encounter = service.get(db, patient, encounter_id)
    return handoff.build(db, patient, encounter)


@router.get(
    "/{encounter_id}/handoff.svg",
    responses={200: {"content": {"image/svg+xml": {}}}},
    response_class=Response,
)
def visit_handoff_qr(
    encounter_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> Response:
    """A QR code the clinician scans.

    Carries a link to the summary page when a public web address is
    configured, and the visit data itself otherwise. `X-Handoff-Kind` says
    which, so the screen can explain what will happen when it is scanned.
    """
    encounter = service.get(db, patient, encounter_id)
    svg, kind = handoff.code_for(db, patient, encounter)
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            # Never cached: a link expires, a payload carries a timestamp, and
            # neither belongs in a proxy that serves other people.
            "Cache-Control": "no-store",
            "X-Handoff-Kind": kind,
        },
    )


@router.get("/handoff/{token}")
def scanned_handoff(token: str, db: Session = Depends(get_db)) -> dict:
    """The visit summary, for whoever scanned the code.

    Deliberately unauthenticated: the clinician holding the phone has no
    account here, and asking them to make one at the moment of a consultation
    would defeat the point. The token in the URL *is* the credential — it
    grants read access to exactly this one visit and expires within the hour.

    Nothing is trimmed here. That is the advantage of a link over a code that
    carries its own data: a page can show every answer and every finding.

    @raises AuthenticationError when the token is missing, altered, expired,
            or is not a handoff token.
    """
    try:
        encounter_id = uuid.UUID(handoff.decode_handoff_token(token))
    except (jwt.PyJWTError, ValueError):
        raise AuthenticationError(
            "This code has expired. Please ask the patient to show a new one."
        )

    encounter = service.get_for_handoff(db, encounter_id)
    return handoff.build(db, encounter.patient, encounter, fit=False)
