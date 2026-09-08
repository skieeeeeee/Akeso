"""Interview API contracts."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import Field

from app.shared.enums import AnswerKind, ConversationStatus, InputMethod, Language
from app.shared.schemas import ApiModel


class StartInterviewIn(ApiModel):
    # AYUSH is opt-in; nothing else is optional.
    include_ayush: bool = False


class QuestionOption(ApiModel):
    value: str
    label: str
    icon: str | None = None


class QuestionView(ApiModel):
    """One question, already localised and mode-adapted server-side."""

    id: str
    instance_key: str
    section: str
    section_title: str
    section_intro: str
    kind: AnswerKind
    text: str
    help: str
    options: list[QuestionOption] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    allow_none: bool = True
    required: bool = False
    # True when this question came from an AI suggestion, so the UI can label it.
    is_ai_suggested: bool = False
    # Non-empty for a per-item follow-up, e.g. "Diabetes".
    about: str = ""


class ProgressView(ApiModel):
    answered: int
    total: int
    percent: int
    section: str
    section_index: int
    section_count: int


class InterviewView(ApiModel):
    session_id: uuid.UUID
    status: ConversationStatus
    question: QuestionView | None
    progress: ProgressView
    complete: bool
    # Set when the last answer could not be used and is being asked again.
    retry_hint: str | None = None
    # True when AI assistance is unavailable and deterministic rules are in use.
    ai_fallback_active: bool = False
    language: Language


class AnswerIn(ApiModel):
    # Which question this answers; guards against a stale screen.
    instance_key: str = Field(min_length=1, max_length=200)
    text: str = Field(default="", max_length=2000)
    input_method: InputMethod = InputMethod.TEXT


class AnswerRecord(ApiModel):
    question_id: str
    question_text: str
    section: str
    raw_answer: str
    normalized_answer: str
    input_method: InputMethod
    extracted_items: list[str]
    ai_assisted: bool
    created_at: datetime


class TranscriptView(ApiModel):
    session_id: uuid.UUID
    answers: list[AnswerRecord]


class StructuredHistoryView(ApiModel):
    """The generated history, split by where each fact came from."""

    sections: dict[str, list[dict[str, Any]]]
    patient_reported_count: int
    document_derived_count: int
    missing_sections: list[str]
    narrative: str | None
    narrative_source: str
    ayush_included: bool
