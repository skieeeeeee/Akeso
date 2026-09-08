"""Deterministic experience-recommendation engine.

Pure functions, no I/O, no LLM. Given a patient's assessment answers it
returns the recommended interface settings plus patient-readable reasons for
each decision.

Design rules encoded here (from the product spec):

* Age may *influence* the recommendation but can never on its own force Easy
  Mode. The maximum age contribution (2) is below the Easy Mode threshold (3).
* Low digital comfort strongly influences Easy Mode: "I sometimes need help"
  or "I prefer a simpler experience" reaches the threshold alone.
* Reading difficulty increases text size and may enable audio guidance.
* Vision difficulty increases text size and enables high contrast.
* Hearing difficulty must never leave the experience dependent on audio, so
  it disables audio guidance outright.
* Low literacy enables audio guidance, icon support and simplified language.
* Nothing here is a diagnosis, and no sensitive information is inferred.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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

# --- Tunable weights -------------------------------------------------------

EASY_MODE_THRESHOLD = 3

DIGITAL_COMFORT_WEIGHT: dict[DigitalComfort, int] = {
    DigitalComfort.VERY_COMFORTABLE: 0,
    DigitalComfort.SOMEWHAT_COMFORTABLE: 1,
    DigitalComfort.NEED_HELP: 3,
    DigitalComfort.PREFER_SIMPLE: 4,
}

DIFFICULTY_WEIGHT: dict[DifficultyLevel, int] = {
    DifficultyLevel.NONE: 0,
    DifficultyLevel.SOMETIMES: 1,
    DifficultyLevel.YES: 2,
}

# Deliberately capped below EASY_MODE_THRESHOLD.
AGE_WEIGHT_BANDS: tuple[tuple[int, int], ...] = ((80, 2), (70, 1))
MAX_AGE_WEIGHT = max(weight for _, weight in AGE_WEIGHT_BANDS)

NEED_EASY_WEIGHT: dict[AccessibilityNeed, int] = {
    AccessibilityNeed.LOW_LITERACY: 3,
    AccessibilityNeed.NEEDS_ASSISTANT: 2,
}

_FONT_ORDER: tuple[FontSize, ...] = (
    FontSize.NORMAL,
    FontSize.LARGE,
    FontSize.EXTRA_LARGE,
)


def _at_least(current: FontSize, minimum: FontSize) -> FontSize:
    return max(current, minimum, key=_FONT_ORDER.index)


def age_weight(age: int | None) -> int:
    if age is None:
        return 0
    for threshold, weight in AGE_WEIGHT_BANDS:
        if age >= threshold:
            return weight
    return 0


# --- Inputs and outputs ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class Reason:
    """A patient-facing explanation for one part of the recommendation."""

    code: str
    en: str
    hi: str

    def text(self, language: Language) -> str:
        return self.hi if language == Language.HINDI else self.en

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "en": self.en, "hi": self.hi}


@dataclass(frozen=True, slots=True)
class AssessmentAnswers:
    digital_comfort: DigitalComfort
    preferred_interaction: PreferredInteraction
    reading_difficulty: DifficultyLevel
    hearing_difficulty: DifficultyLevel
    vision_difficulty: DifficultyLevel
    additional_needs: tuple[AccessibilityNeed, ...] = ()
    age: int | None = None
    language: Language = Language.ENGLISH


@dataclass(frozen=True, slots=True)
class Recommendation:
    interface_mode: InterfaceMode
    font_size: FontSize
    contrast_mode: ContrastMode
    audio_guidance: bool
    interaction_preference: InteractionPreference
    language: Language
    easy_mode_score: int
    reasons: tuple[Reason, ...] = field(default=())

    def as_dict(self) -> dict[str, Any]:
        """Serialisable snapshot, stored on the assessment row."""
        return {
            "interface_mode": self.interface_mode.value,
            "font_size": self.font_size.value,
            "contrast_mode": self.contrast_mode.value,
            "audio_guidance": self.audio_guidance,
            "interaction_preference": self.interaction_preference.value,
            "language": self.language.value,
            "easy_mode_score": self.easy_mode_score,
            "easy_mode_threshold": EASY_MODE_THRESHOLD,
            "reasons": [reason.as_dict() for reason in self.reasons],
        }


# --- The engine ------------------------------------------------------------


def recommend_experience(answers: AssessmentAnswers) -> Recommendation:
    needs = set(answers.additional_needs)
    reasons: list[Reason] = []

    # ---- Interface mode ---------------------------------------------------
    score = (
        DIGITAL_COMFORT_WEIGHT[answers.digital_comfort]
        + DIFFICULTY_WEIGHT[answers.reading_difficulty]
        + DIFFICULTY_WEIGHT[answers.vision_difficulty]
        + age_weight(answers.age)
        + sum(NEED_EASY_WEIGHT.get(need, 0) for need in needs)
    )
    interface_mode = (
        InterfaceMode.EASY if score >= EASY_MODE_THRESHOLD else InterfaceMode.STANDARD
    )

    if interface_mode == InterfaceMode.EASY:
        if DIGITAL_COMFORT_WEIGHT[answers.digital_comfort] >= 3:
            reasons.append(
                Reason(
                    "easy_mode_digital_comfort",
                    "You told us you prefer a simpler experience, so we will show one question at a time with large buttons.",
                    "आपने बताया कि आपको आसान अनुभव पसंद है, इसलिए हम एक बार में एक सवाल और बड़े बटन दिखाएंगे।",
                )
            )
        else:
            reasons.append(
                Reason(
                    "easy_mode_combined",
                    "Based on your answers we have set up a simpler experience with larger buttons and one question at a time.",
                    "आपके जवाबों के आधार पर हमने बड़े बटन और एक बार में एक सवाल वाला आसान अनुभव तैयार किया है।",
                )
            )
    else:
        reasons.append(
            Reason(
                "standard_mode",
                "You seem comfortable with digital forms, so we have kept the standard experience.",
                "आप डिजिटल फ़ॉर्म में सहज लगते हैं, इसलिए हमने सामान्य अनुभव रखा है।",
            )
        )

    # ---- Font size --------------------------------------------------------
    font_size = FontSize.NORMAL
    if answers.vision_difficulty == DifficultyLevel.YES or AccessibilityNeed.LOW_VISION in needs:
        font_size = FontSize.EXTRA_LARGE
        reasons.append(
            Reason(
                "font_vision",
                "You told us screens are hard to see, so we have made the text much larger.",
                "आपने बताया कि स्क्रीन देखने में कठिनाई होती है, इसलिए हमने टेक्स्ट काफ़ी बड़ा कर दिया है।",
            )
        )
    elif answers.vision_difficulty == DifficultyLevel.SOMETIMES:
        font_size = _at_least(font_size, FontSize.LARGE)
        reasons.append(
            Reason(
                "font_vision_sometimes",
                "Since seeing the screen is sometimes difficult, we have increased the text size.",
                "चूंकि स्क्रीन देखने में कभी-कभी कठिनाई होती है, हमने टेक्स्ट का आकार बढ़ा दिया है।",
            )
        )

    if answers.reading_difficulty == DifficultyLevel.YES:
        font_size = _at_least(font_size, FontSize.LARGE)
        reasons.append(
            Reason(
                "font_reading",
                "You told us reading on screens is difficult, so text is larger and we can read questions aloud.",
                "आपने बताया कि स्क्रीन पर पढ़ना कठिन है, इसलिए टेक्स्ट बड़ा है और हम सवाल बोलकर भी सुना सकते हैं।",
            )
        )

    if answers.age is not None and answers.age >= 75:
        font_size = _at_least(font_size, FontSize.LARGE)
    if interface_mode == InterfaceMode.EASY:
        font_size = _at_least(font_size, FontSize.LARGE)

    # ---- Contrast ---------------------------------------------------------
    needs_high_contrast = (
        answers.vision_difficulty in (DifficultyLevel.SOMETIMES, DifficultyLevel.YES)
        or AccessibilityNeed.LOW_VISION in needs
    )
    contrast_mode = ContrastMode.HIGH if needs_high_contrast else ContrastMode.NORMAL
    if needs_high_contrast:
        reasons.append(
            Reason(
                "contrast_high",
                "We have turned on stronger colour contrast to make content easier to see.",
                "सामग्री देखने में आसानी के लिए हमने अधिक रंग कंट्रास्ट चालू कर दिया है।",
            )
        )

    # ---- Audio guidance ---------------------------------------------------
    hearing_limited = (
        answers.hearing_difficulty == DifficultyLevel.YES
        or AccessibilityNeed.HARD_OF_HEARING in needs
    )
    would_benefit_from_audio = (
        answers.reading_difficulty in (DifficultyLevel.SOMETIMES, DifficultyLevel.YES)
        or answers.vision_difficulty == DifficultyLevel.YES
        or AccessibilityNeed.LOW_LITERACY in needs
        or answers.digital_comfort
        in (DigitalComfort.NEED_HELP, DigitalComfort.PREFER_SIMPLE)
        or answers.preferred_interaction
        in (PreferredInteraction.SPEAKING, PreferredInteraction.BOTH)
    )

    if hearing_limited:
        # Never make the experience depend on sound.
        audio_guidance = False
        reasons.append(
            Reason(
                "audio_off_hearing",
                "Because hearing audio is difficult, nothing in this app needs sound — every instruction is written on screen.",
                "सुनने में कठिनाई के कारण, इस ऐप में कुछ भी आवाज़ पर निर्भर नहीं है — हर निर्देश स्क्रीन पर लिखा होगा।",
            )
        )
    elif would_benefit_from_audio:
        audio_guidance = True
        reasons.append(
            Reason(
                "audio_on",
                "We will read questions aloud. You can switch this off at any time.",
                "हम सवाल बोलकर सुनाएंगे। आप इसे कभी भी बंद कर सकते हैं।",
            )
        )
    else:
        audio_guidance = False

    # ---- Interaction preference -------------------------------------------
    base_interaction = {
        PreferredInteraction.SPEAKING: InteractionPreference.VOICE,
        PreferredInteraction.TOUCHING: InteractionPreference.TOUCH,
        PreferredInteraction.BOTH: InteractionPreference.HYBRID,
    }[answers.preferred_interaction]

    interaction_preference = base_interaction
    if (
        base_interaction == InteractionPreference.TOUCH
        and answers.reading_difficulty == DifficultyLevel.YES
    ):
        # Reading is hard, so keep speaking available even though they chose touch.
        interaction_preference = InteractionPreference.HYBRID
        reasons.append(
            Reason(
                "interaction_hybrid_reading",
                "You can tap your answers, and speak them instead whenever that is easier.",
                "आप अपने जवाब छू कर चुन सकते हैं, और जब आसान लगे तब बोलकर भी बता सकते हैं।",
            )
        )
    elif (
        base_interaction == InteractionPreference.TOUCH
        and AccessibilityNeed.LIMITED_HAND_MOBILITY in needs
    ):
        interaction_preference = InteractionPreference.HYBRID
        reasons.append(
            Reason(
                "interaction_hybrid_mobility",
                "Speaking is available alongside tapping, in case tapping is tiring.",
                "छूने के साथ बोलने का विकल्प भी उपलब्ध है, यदि छूना थकाऊ लगे।",
            )
        )
    elif (
        base_interaction == InteractionPreference.VOICE
        and AccessibilityNeed.PREFERS_SIGN_LANGUAGE in needs
    ):
        # Do not route a sign-language user through a voice-only path.
        interaction_preference = InteractionPreference.HYBRID

    if interaction_preference == InteractionPreference.VOICE:
        reasons.append(
            Reason(
                "interaction_voice",
                "You can answer by speaking. Typing and tapping stay available as a fallback.",
                "आप बोलकर जवाब दे सकते हैं। टाइप करना और छूना विकल्प के रूप में उपलब्ध रहेगा।",
            )
        )

    return Recommendation(
        interface_mode=interface_mode,
        font_size=font_size,
        contrast_mode=contrast_mode,
        audio_guidance=audio_guidance,
        interaction_preference=interaction_preference,
        language=answers.language,
        easy_mode_score=score,
        reasons=tuple(reasons),
    )
