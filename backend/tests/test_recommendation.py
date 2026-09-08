"""The recommendation engine is pure, so it is tested directly and exhaustively.

These tests encode the product rules, not the implementation — they are the
ones that must not be quietly relaxed.
"""

from __future__ import annotations

import pytest

from app.modules.accessibility.recommendation import (
    EASY_MODE_THRESHOLD,
    MAX_AGE_WEIGHT,
    AssessmentAnswers,
    recommend_experience,
)
from app.shared.enums import (
    AccessibilityNeed,
    ContrastMode,
    DifficultyLevel,
    DigitalComfort,
    FontSize,
    InteractionPreference,
    InterfaceMode,
    Language,
    PreferredInteraction,
)


def answers(**overrides) -> AssessmentAnswers:
    """A digitally-comfortable patient with no reported difficulty."""
    base = {
        "digital_comfort": DigitalComfort.VERY_COMFORTABLE,
        "preferred_interaction": PreferredInteraction.TOUCHING,
        "reading_difficulty": DifficultyLevel.NONE,
        "hearing_difficulty": DifficultyLevel.NONE,
        "vision_difficulty": DifficultyLevel.NONE,
    }
    return AssessmentAnswers(**{**base, **overrides})


class TestAgeNeverForcesEasyMode:
    """Age may influence the result but must never decide it alone."""

    def test_age_weight_cannot_reach_the_threshold(self):
        assert MAX_AGE_WEIGHT < EASY_MODE_THRESHOLD

    @pytest.mark.parametrize("age", [65, 70, 75, 80, 95, 105])
    def test_age_alone_keeps_standard_mode(self, age: int):
        result = recommend_experience(answers(age=age))
        assert result.interface_mode == InterfaceMode.STANDARD

    def test_age_still_enlarges_text_for_the_very_old(self):
        assert recommend_experience(answers(age=78)).font_size == FontSize.LARGE
        assert recommend_experience(answers(age=60)).font_size == FontSize.NORMAL

    def test_age_tips_the_balance_when_combined(self):
        # Somewhat comfortable (1) + sometimes reading (1) = 2, below threshold.
        assert recommend_experience(
            answers(
                digital_comfort=DigitalComfort.SOMEWHAT_COMFORTABLE,
                reading_difficulty=DifficultyLevel.SOMETIMES,
            )
        ).interface_mode == InterfaceMode.STANDARD
        # The same answers at 82 reach it.
        assert recommend_experience(
            answers(
                digital_comfort=DigitalComfort.SOMEWHAT_COMFORTABLE,
                reading_difficulty=DifficultyLevel.SOMETIMES,
                age=82,
            )
        ).interface_mode == InterfaceMode.EASY


class TestDigitalComfort:
    """Low digital comfort should strongly influence Easy Mode."""

    @pytest.mark.parametrize(
        "comfort,expected",
        [
            (DigitalComfort.VERY_COMFORTABLE, InterfaceMode.STANDARD),
            (DigitalComfort.SOMEWHAT_COMFORTABLE, InterfaceMode.STANDARD),
            (DigitalComfort.NEED_HELP, InterfaceMode.EASY),
            (DigitalComfort.PREFER_SIMPLE, InterfaceMode.EASY),
        ],
    )
    def test_comfort_alone_decides(self, comfort, expected):
        assert recommend_experience(answers(digital_comfort=comfort)).interface_mode == expected

    def test_easy_mode_always_enlarges_text(self):
        result = recommend_experience(answers(digital_comfort=DigitalComfort.PREFER_SIMPLE))
        assert result.interface_mode == InterfaceMode.EASY
        assert result.font_size in (FontSize.LARGE, FontSize.EXTRA_LARGE)


class TestVision:
    def test_difficulty_seeing_maximises_text_and_contrast(self):
        result = recommend_experience(answers(vision_difficulty=DifficultyLevel.YES))
        assert result.font_size == FontSize.EXTRA_LARGE
        assert result.contrast_mode == ContrastMode.HIGH

    def test_occasional_difficulty_is_a_softer_response(self):
        result = recommend_experience(answers(vision_difficulty=DifficultyLevel.SOMETIMES))
        assert result.font_size == FontSize.LARGE
        assert result.contrast_mode == ContrastMode.HIGH

    def test_declared_low_vision_need_is_honoured(self):
        result = recommend_experience(
            answers(additional_needs=(AccessibilityNeed.LOW_VISION,))
        )
        assert result.font_size == FontSize.EXTRA_LARGE
        assert result.contrast_mode == ContrastMode.HIGH

    def test_no_vision_difficulty_keeps_normal_contrast(self):
        assert recommend_experience(answers()).contrast_mode == ContrastMode.NORMAL


class TestReading:
    def test_reading_difficulty_enlarges_text_and_enables_audio(self):
        result = recommend_experience(answers(reading_difficulty=DifficultyLevel.YES))
        assert result.font_size in (FontSize.LARGE, FontSize.EXTRA_LARGE)
        assert result.audio_guidance is True

    def test_reading_difficulty_keeps_speaking_available(self):
        # Patient chose touch, but reading is hard — speaking stays offered.
        result = recommend_experience(
            answers(
                preferred_interaction=PreferredInteraction.TOUCHING,
                reading_difficulty=DifficultyLevel.YES,
            )
        )
        assert result.interaction_preference == InteractionPreference.HYBRID


class TestHearing:
    """Hearing difficulty must never leave the experience dependent on audio."""

    def test_hearing_difficulty_disables_audio(self):
        result = recommend_experience(answers(hearing_difficulty=DifficultyLevel.YES))
        assert result.audio_guidance is False

    def test_hearing_difficulty_wins_over_every_audio_trigger(self):
        result = recommend_experience(
            answers(
                hearing_difficulty=DifficultyLevel.YES,
                reading_difficulty=DifficultyLevel.YES,
                vision_difficulty=DifficultyLevel.YES,
                digital_comfort=DigitalComfort.PREFER_SIMPLE,
                preferred_interaction=PreferredInteraction.SPEAKING,
                additional_needs=(AccessibilityNeed.LOW_LITERACY,),
            )
        )
        assert result.audio_guidance is False
        # ...but the visual accommodations still apply.
        assert result.font_size == FontSize.EXTRA_LARGE
        assert result.interface_mode == InterfaceMode.EASY

    def test_declared_hard_of_hearing_also_disables_audio(self):
        result = recommend_experience(
            answers(
                reading_difficulty=DifficultyLevel.YES,
                additional_needs=(AccessibilityNeed.HARD_OF_HEARING,),
            )
        )
        assert result.audio_guidance is False


class TestLowLiteracy:
    def test_low_literacy_enables_easy_mode_and_audio(self):
        result = recommend_experience(
            answers(additional_needs=(AccessibilityNeed.LOW_LITERACY,))
        )
        assert result.interface_mode == InterfaceMode.EASY
        assert result.audio_guidance is True


class TestInteraction:
    @pytest.mark.parametrize(
        "preferred,expected",
        [
            (PreferredInteraction.SPEAKING, InteractionPreference.VOICE),
            (PreferredInteraction.TOUCHING, InteractionPreference.TOUCH),
            (PreferredInteraction.BOTH, InteractionPreference.HYBRID),
        ],
    )
    def test_patient_choice_is_respected(self, preferred, expected):
        assert (
            recommend_experience(answers(preferred_interaction=preferred)).interaction_preference
            == expected
        )

    def test_limited_hand_mobility_offers_speaking_too(self):
        result = recommend_experience(
            answers(additional_needs=(AccessibilityNeed.LIMITED_HAND_MOBILITY,))
        )
        assert result.interaction_preference == InteractionPreference.HYBRID

    def test_sign_language_user_is_not_routed_to_voice_only(self):
        result = recommend_experience(
            answers(
                preferred_interaction=PreferredInteraction.SPEAKING,
                additional_needs=(AccessibilityNeed.PREFERS_SIGN_LANGUAGE,),
            )
        )
        assert result.interaction_preference != InteractionPreference.VOICE


class TestOutputContract:
    def test_language_passes_through(self):
        assert recommend_experience(answers(language=Language.HINDI)).language == Language.HINDI

    def test_every_recommendation_explains_itself(self):
        result = recommend_experience(answers(vision_difficulty=DifficultyLevel.YES))
        assert result.reasons, "the patient must be told why"
        for reason in result.reasons:
            assert reason.code
            assert reason.en and reason.hi, f"{reason.code} is missing a translation"

    def test_snapshot_is_json_serialisable(self):
        import json

        snapshot = recommend_experience(answers()).as_dict()
        json.dumps(snapshot)  # must not raise
        assert snapshot["easy_mode_threshold"] == EASY_MODE_THRESHOLD

    def test_engine_is_deterministic(self):
        given = answers(
            digital_comfort=DigitalComfort.NEED_HELP,
            reading_difficulty=DifficultyLevel.SOMETIMES,
            age=68,
        )
        first = recommend_experience(given)
        for _ in range(20):
            assert recommend_experience(given) == first

    def test_missing_age_is_handled(self):
        result = recommend_experience(answers(age=None))
        assert result.interface_mode == InterfaceMode.STANDARD
