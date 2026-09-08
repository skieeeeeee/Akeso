"""Strict schemas for every AI output.

Nothing a model produces reaches the database or the UI without validating
against one of these. A model that returns anything else is treated exactly
like an outage: the caller falls back to its deterministic path.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums import ExtractedEntityType, LabFlag


class Strict(BaseModel):
    # Unknown keys are a signal the model improvised — reject rather than absorb.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# --- Understanding a patient's answer -------------------------------------


class ExtractedFact(Strict):
    """One clinical fact the model believes the patient stated."""

    value: str = Field(min_length=1, max_length=200)
    # Which medical-profile section this belongs in.
    section: str = Field(min_length=1, max_length=60)
    attributes: dict[str, str] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0, default=0.6)


class AnswerUnderstanding(Strict):
    """Result of interpreting one free-text/voice answer."""

    facts: list[ExtractedFact] = Field(default_factory=list, max_length=12)
    # True when the patient effectively said "none" / "nothing".
    is_negative: bool = False
    # True when the answer did not address the question at all.
    is_unclear: bool = False


class SuggestedQuestion(Strict):
    """A follow-up the model proposes. The engine decides whether to use it."""

    text_en: str = Field(min_length=5, max_length=200)
    text_hi: str = Field(min_length=3, max_length=240)
    # Which structured field the answer would populate.
    section: str = Field(min_length=1, max_length=60)
    reason: str = Field(default="", max_length=200)


class FollowUpSuggestions(Strict):
    questions: list[SuggestedQuestion] = Field(default_factory=list, max_length=3)


# --- Document intelligence -------------------------------------------------


class DocumentEntity(Strict):
    entity_type: ExtractedEntityType
    value: str = Field(min_length=1, max_length=200)
    # Medication dose/frequency/duration, investigation unit/range, etc.
    attributes: dict[str, str] = Field(default_factory=dict)
    # Only for investigations, and only when a range was printed.
    numeric_value: str | None = Field(default=None, max_length=40)
    unit: str | None = Field(default=None, max_length=40)
    reference_range: str | None = Field(default=None, max_length=60)
    event_date: str | None = Field(default=None, max_length=32)
    confidence: float = Field(ge=0.0, le=1.0, default=0.6)


class DocumentExtraction(Strict):
    document_date: str | None = Field(default=None, max_length=32)
    document_kind: str | None = Field(default=None, max_length=40)
    entities: list[DocumentEntity] = Field(default_factory=list, max_length=80)


# --- Summarising -----------------------------------------------------------


class HistorySummary(Strict):
    """Prose summary of information the patient already gave us."""

    summary_en: str = Field(min_length=20, max_length=1800)
    summary_hi: str = Field(default="", max_length=2200)


LAB_FLAG_VALUES = {flag.value for flag in LabFlag}
