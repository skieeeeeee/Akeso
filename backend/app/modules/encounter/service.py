"""Encounter (new visit) use cases.

The returning-patient principle in code: this service asks only about the
current concern, reads the medical profile as read-only context, and writes
today's answers to `Encounter.structured_history`. The profile is never
mutated here, so a visit cannot overwrite the patient's history.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.documents.models import Document
from app.modules.encounter.models import Encounter
from app.modules.encounter.schemas import (
    ConfirmEncounterIn,
    EncounterAnswerIn,
    ExistingContext,
    StartVisitIn,
)
from app.modules.encounter.script import (
    AYUSH_SECTION_KEYS,
    ENCOUNTER_SCRIPT,
    SCREENED_QUESTION_IDS,
    SHARED_AYUSH_SECTION_KEYS,
    ayush_target,
)
from app.modules.interview import engine
from app.modules.interview.models import ConversationAnswer, ConversationSession
from app.modules.interview.schemas import ProgressView, QuestionOption, QuestionView
from app.modules.medical_history import service as medical_service
from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS
from app.modules.patient.models import Patient
from app.modules.red_flags import service as red_flag_service
from app.shared.clinical import ClinicalItem, parse_items
from app.shared.enums import (
    PARTIAL_AYUSH_SYSTEMS,
    AnswerKind,
    CareSystem,
    ClinicalSource,
    ConversationStatus,
    EncounterStatus,
    Language,
    RedFlagStatus,
    VisitType,
)
from app.shared.errors import ConflictError, NotFoundError, ValidationFailedError
from app.shared.i18n import Localised, language_code, localise, t

log = logging.getLogger("medikiosk.encounter")

RETRY_HINT: Localised = t(
    "Sorry, I did not catch that. Please try again, or tap an option.",
    "माफ़ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बताएं, या कोई विकल्प चुनें।",
)

NONE_REPORTED = engine.NONE_REPORTED


# --- Lookup ----------------------------------------------------------------


def get(db: Session, patient: Patient, encounter_id: uuid.UUID) -> Encounter:
    encounter = db.scalar(
        select(Encounter)
        .where(Encounter.id == encounter_id, Encounter.patient_id == patient.id)
        .options(selectinload(Encounter.red_flags), selectinload(Encounter.documents))
    )
    if encounter is None:
        raise NotFoundError("Visit")
    return encounter


def get_for_handoff(db: Session, encounter_id: uuid.UUID) -> Encounter:
    """One visit, looked up without a patient to scope it.

    Every other read here is scoped by patient, which is what stops one
    patient reading another's record. This one cannot be: the caller is a
    clinician with no account, holding a signed token that names this single
    encounter. The token is the authorisation, so it must be verified before
    calling this — and this function is deliberately named so that a future
    reader cannot mistake it for a general-purpose lookup.
    """
    encounter = db.scalar(
        select(Encounter)
        .where(Encounter.id == encounter_id)
        .options(selectinload(Encounter.red_flags), selectinload(Encounter.documents))
    )
    if encounter is None:
        raise NotFoundError("Visit")
    return encounter


def active_encounter(db: Session, patient: Patient) -> Encounter | None:
    """The visit still being filled in, if any. Resuming beats restarting."""
    return db.scalar(
        select(Encounter)
        .where(
            Encounter.patient_id == patient.id,
            Encounter.submitted_at.is_(None),
            Encounter.status.in_(
                [EncounterStatus.DRAFT, EncounterStatus.IN_PROGRESS]
            ),
        )
        .options(selectinload(Encounter.red_flags), selectinload(Encounter.documents))
        .order_by(Encounter.created_at.desc())
        .limit(1)
    )


def _session_for(db: Session, encounter: Encounter) -> ConversationSession:
    session = db.scalar(
        select(ConversationSession).where(
            ConversationSession.encounter_id == encounter.id
        )
    )
    if session is None:
        state = engine.InterviewState(script_name="encounter")
        state.current_section = ENCOUNTER_SCRIPT.section_order[0]
        session = ConversationSession(
            patient_id=encounter.patient_id,
            encounter_id=encounter.id,
            current_section=state.current_section,
            state=state.to_json(),
        )
        db.add(session)
        db.flush()
    return session


# --- Existing (read-only) context -----------------------------------------


def _values(items: list[ClinicalItem], limit: int = 8) -> list[str]:
    return [item.value for item in items if item.value != NONE_REPORTED][:limit]


def existing_context(db: Session, patient: Patient, encounter: Encounter | None = None) -> ExistingContext:
    """What we already know. Read-only — this is why we do not re-ask it."""
    profile = medical_service.ensure_profile(db, patient)
    sections = medical_service.read_sections(profile)

    documents = list(
        db.scalars(
            select(Document)
            .where(Document.patient_id == patient.id)
            .order_by(Document.created_at.desc())
            .limit(3)
        ).all()
    )

    previous = db.scalar(
        select(Encounter)
        .where(
            Encounter.patient_id == patient.id,
            Encounter.submitted_at.is_not(None),
            Encounter.id != (encounter.id if encounter else uuid.uuid4()),
        )
        .order_by(Encounter.submitted_at.desc())
        .limit(1)
    )

    return ExistingContext(
        conditions=_values(sections["past_medical_history"]),
        medications=_values(sections["current_medications"]),
        allergies=_values(sections["allergies"]),
        recent_documents=[
            {
                "id": str(document.id),
                "title": document.title or document.file_name,
                "type": document.document_type.value,
                "date": document.document_date.isoformat() if document.document_date else None,
                "status": document.processing_status.value,
            }
            for document in documents
        ],
        last_visit_at=previous.submitted_at if previous else None,
        last_visit_complaint=previous.chief_complaint if previous else None,
    )


# --- Start -----------------------------------------------------------------


def start(db: Session, patient: Patient, payload: StartVisitIn) -> Encounter:
    """Begin a visit, or resume the one in progress."""
    encounter = active_encounter(db, patient)
    if encounter is None:
        # A patient with any submitted visit is, by definition, returning.
        previous = db.scalar(
            select(Encounter).where(
                Encounter.patient_id == patient.id,
                Encounter.submitted_at.is_not(None),
            )
        )
        encounter = Encounter(
            patient_id=patient.id,
            status=EncounterStatus.IN_PROGRESS,
            visit_type=VisitType.FOLLOW_UP if previous else VisitType.FIRST_VISIT,
            started_at=datetime.now(UTC),
        )
        db.add(encounter)
        db.flush()

    _session_for(db, encounter)

    if payload.chief_complaint and not encounter.chief_complaint:
        encounter.chief_complaint = payload.chief_complaint.strip()[:500]
        db.flush()
    return encounter


# --- Views -----------------------------------------------------------------


def _question_view(
    scheduled: engine.Scheduled, language: Language, easy: bool
) -> QuestionView:
    lang = language_code(language)
    section = ENCOUNTER_SCRIPT.sections_by_key().get(scheduled.question.section)
    return QuestionView(
        id=scheduled.question.id,
        instance_key=scheduled.key,
        section=scheduled.question.section,
        section_title=localise(section.title, lang) if section else "",
        section_intro=localise(section.intro, lang) if section else "",
        kind=scheduled.question.kind,
        text=scheduled.prompt(lang, easy),
        help=scheduled.help_text(lang),
        options=[
            QuestionOption(
                value=option.value,
                label=localise(option.label, lang),
                icon=option.icon,
            )
            for option in scheduled.question.options
        ],
        suggestions=[
            localise(suggestion, lang) for suggestion in scheduled.question.suggestions
        ],
        allow_none=scheduled.question.allow_none,
        required=scheduled.question.required,
        is_ai_suggested=scheduled.prompt_override is not None,
        about=scheduled.item,
    )


def build_view(
    db: Session,
    patient: Patient,
    encounter: Encounter,
    *,
    retry_hint: str | None = None,
):
    from app.modules.encounter.schemas import EncounterView

    session = _session_for(db, encounter)
    state = engine.InterviewState.from_json(session.state)
    scheduled = engine.next_question(state, ENCOUNTER_SCRIPT)

    if scheduled is not None:
        state.current_section = scheduled.question.section
        state.current_question_id = scheduled.key
    else:
        state.current_question_id = None

    progress = engine.progress(state, ENCOUNTER_SCRIPT)
    session.state = state.to_json()
    session.current_section = state.current_section
    session.current_question_id = state.current_question_id
    session.progress_percent = 100 if scheduled is None else progress.percent
    if scheduled is None and session.status == ConversationStatus.IN_PROGRESS:
        session.status = ConversationStatus.AWAITING_REVIEW
    db.flush()

    easy = bool(patient.preferences and patient.preferences.interface_mode.value == "easy")

    return EncounterView(
        encounter_id=encounter.id,
        session_id=session.id,
        status=encounter.status,
        priority=encounter.priority,
        visit_type=encounter.visit_type,
        care_system=encounter.care_system,
        chief_complaint=encounter.chief_complaint,
        question=_question_view(scheduled, patient.preferred_language, easy) if scheduled else None,
        progress=ProgressView(
            answered=progress.answered,
            total=progress.total,
            percent=100 if scheduled is None else progress.percent,
            section=progress.section,
            section_index=progress.section_index,
            section_count=progress.section_count,
        ),
        complete=scheduled is None,
        retry_hint=retry_hint,
        ai_fallback_active=session.ai_fallback_active,
        safety=red_flag_service.state_for(db, encounter),
        existing=existing_context(db, patient, encounter),
        submitted_at=encounter.submitted_at,
        language=patient.preferred_language,
    )


# --- Answering -------------------------------------------------------------


def _record_today(encounter: Encounter, section: str, values: list[str]) -> None:
    """Write to the ENCOUNTER, not the profile.

    Today's answers live on the encounter so the historical record is never
    silently rewritten by a new visit.
    """
    if section not in MEDICAL_PROFILE_SECTIONS or not values:
        return
    history = dict(encounter.structured_history or {})
    bucket = list(history.get(section) or [])
    known = {str(entry.get("value", "")).lower() for entry in bucket}
    for value in values:
        if value.lower() in known:
            continue
        known.add(value.lower())
        bucket.append(
            {
                "value": value,
                "source": ClinicalSource.PATIENT.value,
                "confidence": 1.0,
                "recorded_at": datetime.now(UTC).isoformat(),
            }
        )
    history[section] = bucket
    # Reassign so SQLAlchemy sees the JSONB change.
    encounter.structured_history = history


def _apply_care_system(
    db: Session,
    patient: Patient,
    encounter: Encounter,
    state: engine.InterviewState,
    answer: str,
) -> None:
    """Record the chosen system and open the sections it calls for.

    Ayurveda opens the full examination; the other AYUSH systems open only
    the diet/lifestyle enquiry, which is genuinely shared, because their own
    examination frameworks are not implemented here.
    """
    try:
        system = CareSystem(answer.strip().lower())
    except ValueError:
        return

    encounter.care_system = system
    # Remembered so the next visit pre-selects it rather than asking cold.
    patient.preferred_care_system = system

    if system == CareSystem.AYURVEDA:
        opened = AYUSH_SECTION_KEYS
    elif system in PARTIAL_AYUSH_SYSTEMS:
        opened = SHARED_AYUSH_SECTION_KEYS
    else:
        opened = ()

    for key in opened:
        if key not in state.enabled_sections:
            state.enabled_sections.append(key)
    db.flush()


def _screened_texts(db: Session, session: ConversationSession) -> list[str]:
    return [
        answer.raw_answer
        for answer in db.scalars(
            select(ConversationAnswer).where(ConversationAnswer.session_id == session.id)
        ).all()
        if answer.question_id in SCREENED_QUESTION_IDS and answer.raw_answer
    ]


async def answer(
    db: Session, patient: Patient, encounter_id: uuid.UUID, payload: EncounterAnswerIn
):
    encounter = get(db, patient, encounter_id)
    if encounter.is_submitted:
        raise ConflictError("This visit has already been submitted.")

    session = _session_for(db, encounter)
    state = engine.InterviewState.from_json(session.state)
    scheduled = engine.next_question(state, ENCOUNTER_SCRIPT)
    if scheduled is None:
        return build_view(db, patient, encounter)

    # A stale screen must not answer the wrong question.
    if payload.instance_key != scheduled.key:
        return build_view(db, patient, encounter)

    easy = bool(patient.preferences and patient.preferences.interface_mode.value == "easy")
    lang = patient.preferred_language.value
    question_text = scheduled.prompt(lang, easy)

    applied = engine.apply_answer(state, scheduled, payload.text, patient.preferred_language)
    if applied.retry:
        session.state = state.to_json()
        db.flush()
        return build_view(
            db, patient, encounter, retry_hint=localise(RETRY_HINT, lang)
        )

    if scheduled.target and applied.items:
        _record_today(encounter, scheduled.target, applied.items)

    if scheduled.question.id == "e_complaint" and applied.items:
        encounter.chief_complaint = applied.items[0][:500]

    # --- the care system decides how long this interview is --------------
    if scheduled.question.id == "e_care_system" and applied.items:
        _apply_care_system(db, patient, encounter, state, applied.machine)

    # --- AYUSH answers go to the assessment, not the medical profile -----
    ayush = ayush_target(scheduled.question.id)
    if ayush and applied.items:
        field, key = ayush
        from app.modules.ayush import service as ayush_service

        ayush_service.record_answer(
            db, patient, field, key, [item.lower() for item in applied.machine_items]
        )

    db.add(
        ConversationAnswer(
            session_id=session.id,
            question_id=scheduled.question.id,
            question_text=question_text,
            section=scheduled.question.section,
            raw_answer=payload.text,
            normalized_answer=applied.stored,
            input_method=payload.input_method,
            extracted_items=applied.items,
            ai_assisted=False,
        )
    )
    session.state = state.to_json()
    db.flush()

    # --- safety screening -------------------------------------------------
    # Runs on every answer, on the patient's own words from this visit only.
    if scheduled.question.id in SCREENED_QUESTION_IDS or scheduled.question.kind == AnswerKind.SCALE:
        severity = state.answers.get("e_severity")
        try:
            await red_flag_service.evaluate(
                db, encounter, _screened_texts(db, session), severity
            )
        except Exception as exc:  # noqa: BLE001 - screening must never break a visit
            log.warning("red-flag evaluation failed for %s: %s", encounter.id, exc)

    return build_view(db, patient, encounter)


def back(db: Session, patient: Patient, encounter_id: uuid.UUID):
    encounter = get(db, patient, encounter_id)
    if encounter.is_submitted:
        raise ConflictError("This visit has already been submitted.")
    session = _session_for(db, encounter)
    state = engine.InterviewState.from_json(session.state)
    engine.go_back(state, ENCOUNTER_SCRIPT)
    session.status = ConversationStatus.IN_PROGRESS
    session.state = state.to_json()
    db.flush()
    return build_view(db, patient, encounter)


# --- Safety actions --------------------------------------------------------


def acknowledge_safety(db: Session, patient: Patient, encounter_id: uuid.UUID) -> Encounter:
    """The patient has seen the emergency screen and chose to continue.

    This records the acknowledgement only. Priority and red-flag status are
    deliberately left untouched — a patient cannot de-escalate their own
    encounter, so triggering the emergency path is never a way out of the
    interview.
    """
    encounter = get(db, patient, encounter_id)
    if encounter.red_flag_acknowledged_at is None:
        encounter.red_flag_acknowledged_at = datetime.now(UTC)
        db.flush()
    return encounter


def request_assistance(db: Session, patient: Patient, encounter_id: uuid.UUID) -> Encounter:
    """The patient asked for immediate help from the emergency screen."""
    encounter = get(db, patient, encounter_id)
    encounter.assistance_requested_at = datetime.now(UTC)
    if encounter.red_flag_acknowledged_at is None:
        encounter.red_flag_acknowledged_at = datetime.now(UTC)
    db.flush()
    log.info("assistance requested for encounter %s", encounter.id)
    return encounter


# --- Submission ------------------------------------------------------------


def confirm_and_submit(
    db: Session, patient: Patient, encounter_id: uuid.UUID, payload: ConfirmEncounterIn
) -> Encounter:
    """Submit the visit after the patient's explicit confirmation."""
    encounter = get(db, patient, encounter_id)

    # Idempotent: a double-tap or a resubmitted form must not create a second
    # submission or move the timestamp.
    if encounter.is_submitted:
        return encounter

    if not (payload.symptoms_correct and payload.reviewed_information and payload.understands_use):
        raise ValidationFailedError(
            "Please confirm all three statements before submitting."
        )

    if not encounter.chief_complaint:
        raise ValidationFailedError(
            "Please tell us what brings you in before submitting."
        )

    encounter.patient_confirmed = True
    encounter.submitted_at = datetime.now(UTC)
    encounter.completed_at = encounter.submitted_at
    # A flagged visit stays urgent through submission.
    encounter.status = (
        EncounterStatus.AWAITING_REVIEW
        if encounter.red_flag_status == RedFlagStatus.ACTIVE
        else EncounterStatus.COMPLETED
    )

    session = db.scalar(
        select(ConversationSession).where(ConversationSession.encounter_id == encounter.id)
    )
    if session is not None:
        session.status = ConversationStatus.CONFIRMED
        session.completed_at = encounter.submitted_at

    db.flush()
    log.info("encounter %s submitted (priority=%s)", encounter.id, encounter.priority.value)
    return encounter


def today_sections(encounter: Encounter) -> dict[str, list[dict]]:
    return {
        section: list(entries)
        for section, entries in (encounter.structured_history or {}).items()
        if entries
    }


def answers_for(db: Session, encounter: Encounter) -> list[ConversationAnswer]:
    session = db.scalar(
        select(ConversationSession).where(ConversationSession.encounter_id == encounter.id)
    )
    if session is None:
        return []
    return list(
        db.scalars(
            select(ConversationAnswer)
            .where(ConversationAnswer.session_id == session.id)
            .order_by(ConversationAnswer.created_at)
        ).all()
    )
