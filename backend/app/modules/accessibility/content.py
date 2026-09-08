"""Assessment questions and preference option labels.

Localised copy lives here, server-side, so English and Hindi can never drift
apart between the two clients that render them. Adding a language means
extending these dictionaries and the `Language` enum — nothing else.
"""

from __future__ import annotations

from typing import Any

from app.shared.enums import (
    AccessibilityNeed,
    ContrastMode,
    DifficultyLevel,
    DigitalComfort,
    FontSize,
    InteractionPreference,
    InterfaceMode,
    PreferredInteraction,
)
from app.shared.i18n import Localised, localise, t as _t




DIFFICULTY_OPTIONS: list[dict[str, Any]] = [
    {"value": DifficultyLevel.NONE.value, "label": _t("No difficulty", "कोई कठिनाई नहीं"), "icon": "check"},
    {"value": DifficultyLevel.SOMETIMES.value, "label": _t("Sometimes", "कभी-कभी"), "icon": "minus"},
    {"value": DifficultyLevel.YES.value, "label": _t("Yes", "हाँ"), "icon": "alert"},
]

# The assessment. `field` matches the AssessmentIn schema field exactly, so the
# frontend can build the form generically from this payload.
ASSESSMENT_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "digital_comfort",
        "field": "digital_comfort",
        "kind": "single",
        "required": True,
        "prompt": _t(
            "How comfortable are you using smartphones or digital devices?",
            "स्मार्टफोन या डिजिटल उपकरणों का उपयोग करने में आप कितने सहज हैं?",
        ),
        "help": _t(
            "This helps us choose how much detail to show on each screen.",
            "इससे हम तय करते हैं कि हर स्क्रीन पर कितनी जानकारी दिखाई जाए।",
        ),
        "options": [
            {"value": DigitalComfort.VERY_COMFORTABLE.value, "label": _t("Very comfortable", "बहुत सहज"), "icon": "smartphone"},
            {"value": DigitalComfort.SOMEWHAT_COMFORTABLE.value, "label": _t("Somewhat comfortable", "कुछ हद तक सहज"), "icon": "thumbs-up"},
            {"value": DigitalComfort.NEED_HELP.value, "label": _t("I sometimes need help", "मुझे कभी-कभी मदद चाहिए"), "icon": "helping-hand"},
            {"value": DigitalComfort.PREFER_SIMPLE.value, "label": _t("I prefer a simpler experience", "मुझे आसान अनुभव पसंद है"), "icon": "sparkles"},
        ],
    },
    {
        "id": "preferred_interaction",
        "field": "preferred_interaction",
        "kind": "single",
        "required": True,
        "prompt": _t(
            "How would you prefer to answer questions?",
            "आप सवालों के जवाब कैसे देना चाहेंगे?",
        ),
        "help": _t(
            "You can always switch between speaking and tapping later.",
            "आप बाद में बोलने और छूने के बीच कभी भी बदल सकते हैं।",
        ),
        "options": [
            {"value": PreferredInteraction.SPEAKING.value, "label": _t("By speaking", "बोलकर"), "icon": "mic"},
            {"value": PreferredInteraction.TOUCHING.value, "label": _t("By touching options", "विकल्प छूकर"), "icon": "hand"},
            {"value": PreferredInteraction.BOTH.value, "label": _t("Both", "दोनों"), "icon": "layers"},
        ],
    },
    {
        "id": "reading_difficulty",
        "field": "reading_difficulty",
        "kind": "single",
        "required": True,
        "prompt": _t(
            "Do you have difficulty reading text on screens?",
            "क्या आपको स्क्रीन पर लिखा पढ़ने में कठिनाई होती है?",
        ),
        "help": _t(
            "If reading is hard, we can make text larger and read questions aloud.",
            "पढ़ना कठिन हो तो हम टेक्स्ट बड़ा कर सकते हैं और सवाल बोलकर सुना सकते हैं।",
        ),
        "options": DIFFICULTY_OPTIONS,
    },
    {
        "id": "vision_difficulty",
        "field": "vision_difficulty",
        "kind": "single",
        "required": True,
        "prompt": _t(
            "Do you have difficulty seeing content on screens?",
            "क्या आपको स्क्रीन पर सामग्री देखने में कठिनाई होती है?",
        ),
        "help": _t(
            "We can increase the text size and use stronger colour contrast.",
            "हम टेक्स्ट का आकार बढ़ा सकते हैं और अधिक रंग कंट्रास्ट का उपयोग कर सकते हैं।",
        ),
        "options": DIFFICULTY_OPTIONS,
    },
    {
        "id": "hearing_difficulty",
        "field": "hearing_difficulty",
        "kind": "single",
        "required": True,
        "prompt": _t(
            "Do you have difficulty hearing audio instructions?",
            "क्या आपको आवाज़ के निर्देश सुनने में कठिनाई होती है?",
        ),
        "help": _t(
            "If hearing is hard, nothing in this app will depend on sound.",
            "सुनने में कठिनाई हो तो इस ऐप में कुछ भी आवाज़ पर निर्भर नहीं होगा।",
        ),
        "options": DIFFICULTY_OPTIONS,
    },
    {
        "id": "additional_needs",
        "field": "additional_needs",
        "kind": "multiple",
        "required": False,
        "prompt": _t(
            "Is there anything else that would make this easier for you?",
            "क्या कुछ और है जो इसे आपके लिए आसान बनाएगा?",
        ),
        "help": _t(
            "This is completely optional. Share only what you want to.",
            "यह पूरी तरह वैकल्पिक है। केवल वही बताएं जो आप चाहते हैं।",
        ),
        "options": [
            {"value": AccessibilityNeed.LOW_LITERACY.value, "label": _t("I find reading and writing difficult", "मुझे पढ़ना-लिखना कठिन लगता है"), "icon": "book"},
            {"value": AccessibilityNeed.LOW_VISION.value, "label": _t("I have low vision", "मुझे कम दिखाई देता है"), "icon": "eye"},
            {"value": AccessibilityNeed.HARD_OF_HEARING.value, "label": _t("I am hard of hearing", "मुझे सुनने में कठिनाई है"), "icon": "ear"},
            {"value": AccessibilityNeed.LIMITED_HAND_MOBILITY.value, "label": _t("Tapping the screen is tiring", "स्क्रीन छूना थकाऊ लगता है"), "icon": "hand"},
            {"value": AccessibilityNeed.NEEDS_ASSISTANT.value, "label": _t("Someone is helping me today", "आज कोई मेरी मदद कर रहा है"), "icon": "users"},
            {"value": AccessibilityNeed.PREFERS_SIGN_LANGUAGE.value, "label": _t("I use sign language", "मैं सांकेतिक भाषा का उपयोग करता/करती हूँ"), "icon": "signing"},
        ],
    },
]

# Labels for the customise-preferences screen.
PREFERENCE_OPTIONS: dict[str, list[dict[str, Any]]] = {
    "interface_mode": [
        {"value": InterfaceMode.STANDARD.value, "label": _t("Standard", "सामान्य"), "help": _t("All options on one screen", "सभी विकल्प एक स्क्रीन पर")},
        {"value": InterfaceMode.EASY.value, "label": _t("Easy", "आसान"), "help": _t("One question at a time, large buttons", "एक बार में एक सवाल, बड़े बटन")},
    ],
    "font_size": [
        {"value": FontSize.NORMAL.value, "label": _t("Normal", "सामान्य")},
        {"value": FontSize.LARGE.value, "label": _t("Large", "बड़ा")},
        {"value": FontSize.EXTRA_LARGE.value, "label": _t("Extra large", "अतिरिक्त बड़ा")},
    ],
    "contrast_mode": [
        {"value": ContrastMode.NORMAL.value, "label": _t("Normal colours", "सामान्य रंग")},
        {"value": ContrastMode.HIGH.value, "label": _t("High contrast", "उच्च कंट्रास्ट")},
    ],
    "interaction_preference": [
        {"value": InteractionPreference.TOUCH.value, "label": _t("Touch", "छूकर"), "help": _t("Tap to choose answers", "जवाब चुनने के लिए छुएं")},
        {"value": InteractionPreference.VOICE.value, "label": _t("Voice", "बोलकर"), "help": _t("Speak your answers", "अपने जवाब बोलें")},
        {"value": InteractionPreference.HYBRID.value, "label": _t("Both", "दोनों"), "help": _t("Speak or tap, whichever suits", "बोलें या छुएं, जो सुविधाजनक हो")},
    ],
}
