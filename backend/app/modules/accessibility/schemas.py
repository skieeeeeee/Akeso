"""Accessibility assessment and preference contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from app.shared.enums import (
    AccessibilityNeed,
    ContrastMode,
    DifficultyLevel,
    DigitalComfort,
    FontSize,
    InteractionPreference,
    InterfaceMode,
    Language,
    PreferenceSource,
    PreferredInteraction,
)
from app.shared.schemas import ApiModel


class AssessmentIn(ApiModel):
    digital_comfort: DigitalComfort
    preferred_interaction: PreferredInteraction
    reading_difficulty: DifficultyLevel
    hearing_difficulty: DifficultyLevel
    vision_difficulty: DifficultyLevel
    # Voluntary. Never required, never inferred.
    additional_needs: list[AccessibilityNeed] = Field(default_factory=list)
    additional_notes: str | None = Field(default=None, max_length=1000)


class ReasonOut(ApiModel):
    code: str
    en: str
    hi: str


class PreferencesOut(ApiModel):
    interface_mode: InterfaceMode
    font_size: FontSize
    contrast_mode: ContrastMode
    audio_guidance: bool
    interaction_preference: InteractionPreference
    language: Language
    source: PreferenceSource
    updated_at: datetime | None = None


class RecommendationOut(ApiModel):
    """What the engine suggests, plus why — shown before anything is applied."""

    interface_mode: InterfaceMode
    font_size: FontSize
    contrast_mode: ContrastMode
    audio_guidance: bool
    interaction_preference: InteractionPreference
    language: Language
    easy_mode_score: int
    easy_mode_threshold: int
    reasons: list[ReasonOut]


class AssessmentResultOut(ApiModel):
    assessment_id: str
    recommendation: RecommendationOut
    # Preferences are pre-filled from the recommendation but not yet confirmed.
    preferences: PreferencesOut
    onboarding_status: str
    next_route: str


class PreferencesIn(ApiModel):
    """Accept or customise the experience. Any subset may be supplied."""

    interface_mode: InterfaceMode | None = None
    font_size: FontSize | None = None
    contrast_mode: ContrastMode | None = None
    audio_guidance: bool | None = None
    interaction_preference: InteractionPreference | None = None
    language: Language | None = None
    # False when the patient changed something on the recommendation screen.
    accepted_recommendation: bool = True


class AssessmentContentOut(ApiModel):
    questions: list[dict[str, Any]]
    preference_options: dict[str, list[dict[str, Any]]]
