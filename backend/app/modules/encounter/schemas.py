"""Encounter API contracts."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import Field

from app.modules.interview.schemas import ProgressView, QuestionView
from app.modules.red_flags.schemas import RedFlagStateOut
from app.shared.enums import (
    CareSystem,
    EncounterPriority,
    EncounterStatus,
    InputMethod,
    Language,
    VisitType,
)
from app.shared.schemas import ApiModel, UtcModel


class StartVisitIn(ApiModel):
    """Optionally seed the visit with what the patient already typed."""

    chief_complaint: str | None = Field(default=None, max_length=500)
    input_method: InputMethod = InputMethod.TEXT


class EncounterAnswerIn(ApiModel):
    instance_key: str = Field(min_length=1, max_length=200)
    text: str = Field(default="", max_length=2000)
    input_method: InputMethod = InputMethod.TEXT


class ExistingContext(ApiModel):
    """Read-only history shown alongside today's questions.

    Sent so the patient can see we already know it — and so they are never
    asked for it again. Editing any of this happens on the profile screens,
    not here.
    """

    conditions: list[str]
    medications: list[str]
    allergies: list[str]
    recent_documents: list[dict[str, Any]]
    last_visit_at: datetime | None
    last_visit_complaint: str | None


class EncounterView(ApiModel):
    encounter_id: uuid.UUID
    session_id: uuid.UUID | None
    status: EncounterStatus
    priority: EncounterPriority
    visit_type: VisitType
    # Which system of medicine this visit is for; decides the interview length.
    care_system: CareSystem | None
    chief_complaint: str | None
    question: QuestionView | None
    progress: ProgressView
    complete: bool
    retry_hint: str | None = None
    ai_fallback_active: bool = False
    safety: RedFlagStateOut
    existing: ExistingContext
    submitted_at: datetime | None
    language: Language


class TodayAnswer(ApiModel):
    question_text: str
    answer: str
    section: str
    input_method: InputMethod


class EncounterReviewOut(ApiModel):
    """The pre-submission review screen."""

    encounter_id: uuid.UUID
    chief_complaint: str | None
    # What the patient reported during THIS visit.
    today: dict[str, list[dict[str, Any]]]
    today_answers: list[TodayAnswer]
    # Questions the patient chose not to answer. Counted rather than listed,
    # so a review screen is not a wall of "None reported".
    skipped_count: int = 0
    # The 1-10 rating, shown as a metric rather than as another answer row.
    severity: str | None = None
    # Historical information relevant to today, read-only here.
    existing: ExistingContext
    documents_today: list[dict[str, Any]]
    safety: RedFlagStateOut
    priority: EncounterPriority
    narrative: str
    narrative_source: str
    labels: dict[str, str]
    # The Ayurvedic examination, when this visit ran one. Present so a patient
    # who answered thirty-three questions is not shown five.
    ayush: dict[str, Any] | None = None
    missing: list[str]
    disclaimer: dict[str, str]
    submitted_at: datetime | None
    patient_confirmed: bool


class ConfirmEncounterIn(ApiModel):
    """The patient's explicit confirmation before submission."""

    symptoms_correct: bool
    reviewed_information: bool
    understands_use: bool


class EncounterSummaryOut(UtcModel):
    encounter_id: uuid.UUID
    status: EncounterStatus
    priority: EncounterPriority
    submitted_at: datetime | None
    message: dict[str, str]
