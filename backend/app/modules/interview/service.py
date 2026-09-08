"""Interview orchestration.

The engine decides what to ask. This layer persists state, writes clinical
facts to the medical profile, and *optionally* asks the AI layer to help
understand a free-text answer or propose a follow-up.

Every AI call here is wrapped so that a failure is indistinguishable from AI
being switched off: the deterministic path already ran, the answer is already
recorded, and the session continues. `ai_fallback_active` is set so the UI can
say honestly that assistance is unavailable.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.interview import engine
from app.modules.interview.models import ConversationAnswer, ConversationSession
from app.modules.interview.questions import (
    SECTION_BY_KEY,
    SECTION_ORDER,
    Question,
)
from app.modules.interview.schemas import (
    AnswerIn,
    InterviewView,
    ProgressView,
    QuestionOption,
    QuestionView,
    StartInterviewIn,
)
from app.modules.medical_history import service as medical_service
from app.modules.medical_history.models import MEDICAL_PROFILE_SECTIONS
from app.modules.patient.models import Patient
from app.services.ai import get_provider, structured
from app.services.ai import prompts
from app.services.ai.schemas import AnswerUnderstanding, FollowUpSuggestions
from app.shared.clinical import ClinicalItem, dump_items, parse_items
from app.shared.enums import (
    AnswerKind,
    ClinicalSource,
    ConversationStatus,
    InputMethod,
    Language,
)
from app.shared.errors import NotFoundError, ValidationFailedError
from app.shared.i18n import Localised, language_code, localise, t

log = logging.getLogger("medikiosk.interview")

RETRY_HINT: Localised = t(
    "Sorry, I did not catch that. Please try again, or tap an option.",
    "माफ़ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बताएं, या कोई विकल्प चुनें।",
)


# --- Session plumbing ------------------------------------------------------


def _load(db: Session, patient: Patient, session_id: uuid.UUID) -> ConversationSession:
    row = db.scalar(
        select(ConversationSession).where(
            ConversationSession.id == session_id,
            ConversationSession.patient_id == patient.id,
        )
    )
    if row is None:
        raise NotFoundError("Interview session")
    return row


def active_session(db: Session, patient: Patient) -> ConversationSession | None:
    return db.scalar(
        select(ConversationSession)
        .where(
            ConversationSession.patient_id == patient.id,
            ConversationSession.status == ConversationStatus.IN_PROGRESS,
        )
        .order_by(ConversationSession.created_at.desc())
        .limit(1)
    )


def start(db: Session, patient: Patient, payload: StartInterviewIn) -> ConversationSession:
    """Resume an in-progress interview, or begin a new one.

    Resuming is the default so a patient who closed the tab does not lose
    their answers.
    """
    existing = active_session(db, patient)
    if existing is not None:
        if payload.include_ayush:
            state = engine.InterviewState.from_json(existing.state)
            if "ayush" not in state.enabled_sections:
                state.enabled_sections.append("ayush")
                existing.state = state.to_json()
                db.flush()
        return existing

    state = engine.InterviewState()
    if payload.include_ayush:
        state.enabled_sections.append("ayush")

    session = ConversationSession(
        patient_id=patient.id,
        status=ConversationStatus.IN_PROGRESS,
        current_section=SECTION_ORDER[0],
        state=state.to_json(),
    )
    db.add(session)
    db.flush()
    return session


# --- Views -----------------------------------------------------------------


def _question_view(
    scheduled: engine.Scheduled, language: Language, easy: bool
) -> QuestionView:
    lang = language_code(language)
    section = SECTION_BY_KEY.get(scheduled.question.section)
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


def view(
    db: Session,
    session: ConversationSession,
    patient: Patient,
    *,
    retry_hint: str | None = None,
) -> InterviewView:
    state = engine.InterviewState.from_json(session.state)
    scheduled = engine.next_question(state)

    if scheduled is not None:
        state.current_section = scheduled.question.section
        state.current_question_id = scheduled.key
    else:
        state.current_question_id = None

    progress = engine.progress(state)
    session.state = state.to_json()
    session.current_section = state.current_section
    session.current_question_id = state.current_question_id
    session.progress_percent = 100 if scheduled is None else progress.percent
    if scheduled is None and session.status == ConversationStatus.IN_PROGRESS:
        session.status = ConversationStatus.AWAITING_REVIEW
        session.completed_at = datetime.now(UTC)
    db.flush()

    easy = bool(patient.preferences and patient.preferences.interface_mode.value == "easy")
    language = patient.preferred_language

    return InterviewView(
        session_id=session.id,
        status=session.status,
        question=_question_view(scheduled, language, easy) if scheduled else None,
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
        language=language,
    )


# --- Answering -------------------------------------------------------------


async def _understand(
    question: Question, question_text: str, answer: str
) -> AnswerUnderstanding | None:
    """Ask the AI layer to read a free-text answer. None on any failure."""
    provider = get_provider()
    if provider.name == "none":
        return None
    system, prompt = prompts.understand_answer(
        question=question_text,
        answer=answer,
        section=question.target or question.section,
        allowed_sections=list(MEDICAL_PROFILE_SECTIONS),
    )
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=1024)
    except Exception as exc:  # noqa: BLE001 - AI must never break the interview
        log.warning("answer understanding failed: %s", exc)
        return None
    return structured(AnswerUnderstanding, raw)


async def _suggest_follow_ups(
    state: engine.InterviewState, section: str, known: list[str]
) -> FollowUpSuggestions | None:
    provider = get_provider()
    if provider.name == "none":
        return None
    missing = [
        name
        for name in MEDICAL_PROFILE_SECTIONS
        if not any(name in answer for answer in state.answers)
    ][:6]
    system, prompt = prompts.suggest_follow_ups(
        section=section, known_facts=known, missing_sections=missing
    )
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=800)
    except Exception as exc:  # noqa: BLE001
        log.warning("follow-up suggestion failed: %s", exc)
        return None
    return structured(FollowUpSuggestions, raw)


def _write_items(
    db: Session,
    patient: Patient,
    section: str,
    values: list[str],
    *,
    confidence: float = 1.0,
    note: str | None = None,
) -> None:
    """Append clinical items to a medical-profile section, de-duplicated."""
    if section not in MEDICAL_PROFILE_SECTIONS or not values:
        return
    profile = medical_service.ensure_profile(db, patient)
    existing = parse_items(profile.section(section))
    known = {item.value.lower() for item in existing}

    # A real finding supersedes a previously recorded "None reported".
    if any(value != engine.NONE_REPORTED for value in values):
        existing = [item for item in existing if item.value != engine.NONE_REPORTED]
        known = {item.value.lower() for item in existing}

    for value in values:
        if value.lower() in known:
            continue
        known.add(value.lower())
        existing.append(
            ClinicalItem(
                value=value,
                source=ClinicalSource.PATIENT,
                confidence=confidence,
                verified=False,
                note=note,
            )
        )
    setattr(profile, section, dump_items(existing))
    db.flush()


async def answer(
    db: Session, patient: Patient, session_id: uuid.UUID, payload: AnswerIn
) -> InterviewView:
    session = _load(db, patient, session_id)
    if session.status != ConversationStatus.IN_PROGRESS:
        raise ValidationFailedError("This interview has already been completed.")

    state = engine.InterviewState.from_json(session.state)
    scheduled = engine.next_question(state)
    if scheduled is None:
        return view(db, session, patient)

    # Guard against a stale screen answering the wrong question.
    if payload.instance_key != scheduled.key:
        return view(db, session, patient)

    easy = bool(patient.preferences and patient.preferences.interface_mode.value == "easy")
    lang = patient.preferred_language.value
    question_text = scheduled.prompt(lang, easy)

    # --- deterministic pass (always) -------------------------------------
    applied = engine.apply_answer(state, scheduled, payload.text, patient.preferred_language)

    if applied.retry:
        session.state = state.to_json()
        db.flush()
        return view(db, session, patient, retry_hint=localise(RETRY_HINT, lang))

    target = scheduled.target
    if target and applied.items:
        _write_items(db, patient, target, applied.items)

    # --- optional AI pass -------------------------------------------------
    ai_assisted = False
    free_form = scheduled.question.kind in (AnswerKind.FREE_TEXT, AnswerKind.LIST)
    if free_form and applied.items and applied.items != [engine.NONE_REPORTED]:
        understanding = await _understand(scheduled.question, question_text, payload.text)
        if understanding is None:
            # Only flag fallback when a provider was supposed to be there.
            if get_provider().name != "none":
                session.ai_fallback_active = True
        else:
            ai_assisted = True
            session.ai_fallback_active = False
            for fact in understanding.facts:
                # Facts for the current target are already recorded by the
                # deterministic pass; only cross-section facts add anything.
                if fact.section == target or fact.section not in MEDICAL_PROFILE_SECTIONS:
                    continue
                _write_items(
                    db,
                    patient,
                    fact.section,
                    [fact.value],
                    confidence=min(fact.confidence, 0.9),
                    note="understood_from_speech",
                )

            suggestions = await _suggest_follow_ups(
                state, scheduled.question.section, applied.items
            )
            for suggestion in (suggestions.questions if suggestions else [])[:1]:
                if suggestion.section not in MEDICAL_PROFILE_SECTIONS:
                    continue
                engine.enqueue_suggested(
                    state,
                    prompt={"en": suggestion.text_en, "hi": suggestion.text_hi},
                    target=suggestion.section,
                    tag=suggestion.section,
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
            ai_assisted=ai_assisted,
        )
    )
    session.state = state.to_json()
    db.flush()
    return view(db, session, patient)


def back(db: Session, patient: Patient, session_id: uuid.UUID) -> InterviewView:
    """Reopen the previous question so the patient can change their answer."""
    session = _load(db, patient, session_id)
    state = engine.InterviewState.from_json(session.state)
    engine.go_back(state)
    session.status = ConversationStatus.IN_PROGRESS
    session.completed_at = None
    session.state = state.to_json()
    db.flush()
    return view(db, session, patient)


def transcript(db: Session, patient: Patient, session_id: uuid.UUID) -> list[ConversationAnswer]:
    session = _load(db, patient, session_id)
    return list(session.answers)


def confirm(db: Session, patient: Patient, session_id: uuid.UUID) -> ConversationSession:
    session = _load(db, patient, session_id)
    session.status = ConversationStatus.CONFIRMED
    session.completed_at = session.completed_at or datetime.now(UTC)
    db.flush()
    return session


def get(db: Session, patient: Patient, session_id: uuid.UUID) -> ConversationSession:
    return _load(db, patient, session_id)
