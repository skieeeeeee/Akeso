"""Medical profile section metadata.

Drives the onboarding form and the profile screen from one definition, so the
UI never hard-codes a section list that can drift from the database.
"""

from __future__ import annotations

from typing import Any
from app.shared.i18n import Localised, localise, t as _t




# `key` matches the MedicalProfile column and MEDICAL_PROFILE_SECTIONS exactly.
MEDICAL_SECTIONS: list[dict[str, Any]] = [
    {
        "key": "chief_complaint",
        "title": _t("Why you are here", "आप क्यों आए हैं"),
        "prompt": _t("What problem brings you in today?", "आज आप किस तकलीफ़ के लिए आए हैं?"),
        "placeholder": _t("e.g. chest pain for three days", "जैसे तीन दिन से सीने में दर्द"),
        "icon": "stethoscope",
        "important": True,
        "suggestions": [
            _t("Chest pain", "सीने में दर्द"),
            _t("Fever", "बुखार"),
            _t("Headache", "सिर दर्द"),
            _t("Only here for a check-up", "केवल जाँच के लिए"),
        ],
    },
    {
        "key": "history_of_present_illness",
        "title": _t("About this problem", "इस तकलीफ़ के बारे में"),
        "prompt": _t(
            "How long has it been there, and what makes it better or worse?",
            "यह कब से है, और किससे बढ़ता या कम होता है?",
        ),
        "placeholder": _t("e.g. three days, worse on walking", "जैसे तीन दिन, चलने पर बढ़ता है"),
        "icon": "activity",
        "suggestions": [],
    },
    {
        "key": "past_medical_history",
        "title": _t("Past illnesses", "पिछली बीमारियाँ"),
        "prompt": _t("Any long-term illness you have been told you have?", "कोई पुरानी बीमारी जिसके बारे में आपको बताया गया हो?"),
        "placeholder": _t("e.g. diabetes, high blood pressure", "जैसे मधुमेह, उच्च रक्तचाप"),
        "icon": "stethoscope",
        "suggestions": [
            _t("Diabetes", "मधुमेह"),
            _t("High blood pressure", "उच्च रक्तचाप"),
            _t("Asthma", "दमा"),
            _t("Thyroid problem", "थायरॉइड"),
            _t("Heart disease", "हृदय रोग"),
            _t("Tuberculosis", "तपेदिक"),
        ],
    },
    {
        "key": "current_medications",
        "title": _t("Medicines you take", "आपकी दवाइयाँ"),
        "prompt": _t("Which medicines are you taking now?", "आप अभी कौन सी दवाइयाँ ले रहे हैं?"),
        "placeholder": _t("e.g. Metformin 500 mg twice a day", "जैसे मेटफॉर्मिन 500 मि.ग्रा. दिन में दो बार"),
        "icon": "pill",
        "suggestions": [],
    },
    {
        "key": "drug_history",
        "title": _t("Medicine problems", "दवा से दिक्कत"),
        "prompt": _t(
            "Has any medicine ever caused you a problem?",
            "क्या किसी दवा से आपको कभी दिक्कत हुई है?",
        ),
        "placeholder": _t("e.g. aspirin upset my stomach", "जैसे एस्पिरिन से पेट खराब हुआ"),
        "icon": "pill",
        "suggestions": [],
    },
    {
        "key": "allergies",
        "title": _t("Allergies", "एलर्जी"),
        "prompt": _t("Are you allergic to any medicine or food?", "किसी दवा या खाने से एलर्जी है?"),
        "placeholder": _t("e.g. penicillin, peanuts", "जैसे पेनिसिलिन, मूंगफली"),
        "icon": "alert-triangle",
        "important": True,
        "suggestions": [
            _t("No known allergies", "कोई ज्ञात एलर्जी नहीं"),
            _t("Penicillin", "पेनिसिलिन"),
            _t("Sulfa drugs", "सल्फा दवाएँ"),
            _t("Aspirin", "एस्पिरिन"),
        ],
    },
    {
        "key": "surgical_history",
        "title": _t("Operations", "ऑपरेशन"),
        "prompt": _t("Have you had any operation?", "क्या आपका कोई ऑपरेशन हुआ है?"),
        "placeholder": _t("e.g. gallbladder removed, 2019", "जैसे पित्ताशय निकाला गया, 2019"),
        "icon": "scissors",
        "suggestions": [],
    },
    {
        "key": "family_history",
        "title": _t("Family history", "पारिवारिक इतिहास"),
        "prompt": _t("Any illness that runs in your family?", "आपके परिवार में कोई बीमारी चलती है?"),
        "placeholder": _t("e.g. mother has diabetes", "जैसे माँ को मधुमेह है"),
        "icon": "users",
        "suggestions": [],
    },
    {
        "key": "personal_history",
        "title": _t("Daily habits", "दैनिक आदतें"),
        "prompt": _t("Anything about your habits your doctor should know?", "आपकी आदतों के बारे में कुछ जो डॉक्टर को जानना चाहिए?"),
        "placeholder": _t("e.g. non-smoker, vegetarian diet", "जैसे धूम्रपान नहीं, शाकाहारी भोजन"),
        "icon": "activity",
        "suggestions": [
            _t("Non-smoker", "धूम्रपान नहीं"),
            _t("Smoker", "धूम्रपान करता/करती हूँ"),
            _t("No alcohol", "शराब नहीं"),
            _t("Vegetarian diet", "शाकाहारी भोजन"),
        ],
    },
    {
        "key": "previous_investigations",
        "title": _t("Earlier test results", "पिछली जाँच के परिणाम"),
        "prompt": _t("Any recent test result you remember?", "कोई हाल की जाँच का परिणाम जो आपको याद हो?"),
        "placeholder": _t("e.g. HbA1c 8.4% in March", "जैसे मार्च में HbA1c 8.4%"),
        "icon": "flask",
        "suggestions": [],
    },
    {
        "key": "review_of_systems",
        "title": _t("Anything else you feel", "कुछ और जो महसूस हो"),
        "prompt": _t(
            "Are you also feeling anything else?",
            "क्या आपको कुछ और भी महसूस हो रहा है?",
        ),
        "placeholder": _t("e.g. very tired, losing weight", "जैसे बहुत थकान, वज़न घटना"),
        "icon": "message",
        "suggestions": [
            _t("Very tired", "बहुत थकान"),
            _t("Losing weight", "वज़न घट रहा है"),
            _t("Short of breath", "सांस फूलना"),
            _t("Not sleeping well", "नींद ठीक नहीं"),
        ],
    },
    {
        "key": "additional_information",
        "title": _t("Anything else", "कुछ और"),
        "prompt": _t("Anything else you would like your doctor to know?", "कुछ और जो आप अपने डॉक्टर को बताना चाहें?"),
        "placeholder": _t("Optional", "वैकल्पिक"),
        "icon": "message",
        "suggestions": [],
    },
]

SECTION_KEYS: tuple[str, ...] = tuple(section["key"] for section in MEDICAL_SECTIONS)
