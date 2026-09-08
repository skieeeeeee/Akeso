"""The encounter (new-visit) interview script.

This is the heart of the returning-patient principle: it asks ONLY about the
current concern. Nothing here re-asks past medical history, medications,
allergies or family history — those already exist on the medical profile and
are shown to the patient as read-only context instead.

Answers written by this script land on `Encounter.structured_history`, never
on the profile, so today's visit can never silently overwrite the patient's
historical record.
"""

from __future__ import annotations

from app.modules.interview.questions import Option, Question, Section
from app.shared.enums import AnswerKind
from app.shared.i18n import Localised, localise, t as _t




SECTIONS: tuple[Section, ...] = (
    Section(
        key="system",
        title=_t("Type of treatment", "उपचार का प्रकार"),
        intro=_t(
            "First, tell us which kind of care you are here for.",
            "पहले बताएं कि आप किस प्रकार की चिकित्सा के लिए आए हैं।",
        ),
        icon="stethoscope",
    ),
    Section(
        key="today",
        title=_t("Today's concern", "आज की तकलीफ़"),
        intro=_t(
            "Tell us what is troubling you today.",
            "बताएं आज आपको क्या तकलीफ़ है।",
        ),
        icon="stethoscope",
    ),
    Section(
        key="detail",
        title=_t("A few details", "कुछ विवरण"),
        intro=_t(
            "A few questions about this problem only.",
            "केवल इसी तकलीफ़ के बारे में कुछ सवाल।",
        ),
        icon="activity",
    ),
    Section(
        key="changes",
        title=_t("Anything changed?", "कुछ बदला है?"),
        intro=_t(
            "We already have your health history. Just tell us what is new.",
            "आपका स्वास्थ्य इतिहास हमारे पास है। बस बताएं कि नया क्या है।",
        ),
        icon="message",
    ),
)

AYUSH_SECTIONS: tuple[Section, ...] = (
    Section(
        key="ayush_dashavidha",
        title=_t("Ten-fold examination", "दशविध परीक्षा"),
        intro=_t(
            "Dashavidha Pariksha — questions about your constitution.",
            "दशविध परीक्षा — आपकी प्रकृति से जुड़े सवाल।",
        ),
        icon="book",
        optional=True,
    ),
    Section(
        key="ayush_ashtasthana",
        title=_t("Eight-fold examination", "अष्टस्थान परीक्षा"),
        intro=_t(
            "Ashtasthana Pariksha — your practitioner will confirm each of these.",
            "अष्टस्थान परीक्षा — आपके वैद्य इनमें से प्रत्येक की पुष्टि करेंगे।",
        ),
        icon="stethoscope",
        optional=True,
    ),
    Section(
        key="ayush_lifestyle",
        title=_t("Digestion, sleep and routine", "पाचन, नींद और दिनचर्या"),
        intro=_t(
            "Agni, Nidra, Ahara and Vihara — how you eat, sleep and live.",
            "अग्नि, निद्रा, आहार और विहार — आप कैसे खाते, सोते और रहते हैं।",
        ),
        icon="activity",
        optional=True,
    ),
)

SECTIONS = (*SECTIONS, *AYUSH_SECTIONS)

SECTION_BY_KEY = {section.key: section for section in SECTIONS}
SECTION_ORDER = [section.key for section in SECTIONS]

# Enabled by the care-system answer. Only Ayurveda gets the full set; the
# other AYUSH systems share the diet/lifestyle enquiry but their own
# examinations are not implemented, so we do not pretend otherwise.
AYUSH_SECTION_KEYS = tuple(section.key for section in AYUSH_SECTIONS)
SHARED_AYUSH_SECTION_KEYS = ("ayush_lifestyle",)

_YES_NO: tuple[Option, ...] = (
    Option("yes", _t("Yes", "हाँ"), "check"),
    Option("no", _t("No", "नहीं"), "minus"),
)

_SCALE: tuple[Option, ...] = tuple(Option(str(n), _t(str(n), str(n))) for n in range(1, 11))


def _said_yes(question_id: str):
    return lambda answers: answers.get(question_id, "").strip().lower() == "yes"


QUESTIONS: tuple[Question, ...] = (
    Question(
        id="e_care_system",
        section="system",
        kind=AnswerKind.SINGLE_CHOICE,
        required=True,
        allow_none=False,
        prompt=_t(
            "Which kind of treatment are you here for?",
            "आप किस प्रकार के उपचार के लिए आए हैं?",
        ),
        easy_prompt=_t("Which treatment?", "कौन सा उपचार?"),
        help=_t(
            "This decides which questions we ask. You can pick a different one next time.",
            "इससे तय होता है कि हम कौन से सवाल पूछें। अगली बार आप दूसरा चुन सकते हैं।",
        ),
        options=(
            Option("allopathy", _t("Modern medicine (Allopathy)", "आधुनिक चिकित्सा (एलोपैथी)"), "stethoscope"),
            Option("ayurveda", _t("Ayurveda", "आयुर्वेद"), "book"),
            Option("homoeopathy", _t("Homoeopathy", "होम्योपैथी"), "pill"),
            Option("unani", _t("Unani", "यूनानी"), "pill"),
            Option("siddha", _t("Siddha", "सिद्ध"), "pill"),
            Option("yoga_naturopathy", _t("Yoga & Naturopathy", "योग एवं प्राकृतिक चिकित्सा"), "activity"),
            Option("unsure", _t("I am not sure", "मुझे पता नहीं"), "minus"),
        ),
    ),
    Question(
        id="e_complaint",
        section="today",
        kind=AnswerKind.FREE_TEXT,
        target="chief_complaint",
        required=True,
        allow_none=False,
        prompt=_t("What brings you here today?", "आज आप यहाँ किस वजह से आए हैं?"),
        easy_prompt=_t("What is troubling you today?", "आज आपको क्या तकलीफ़ है?"),
        help=_t(
            "In your own words. You can speak instead of typing.",
            "अपने शब्दों में। आप टाइप करने के बजाय बोल भी सकते हैं।",
        ),
        suggestions=(
            _t("Fever", "बुखार"),
            _t("Cough", "खांसी"),
            _t("Pain", "दर्द"),
            _t("Stomach problem", "पेट की समस्या"),
            _t("Headache", "सिर दर्द"),
            _t("Something else", "कुछ और"),
        ),
    ),
    Question(
        id="e_onset",
        section="detail",
        kind=AnswerKind.SINGLE_CHOICE,
        target="history_of_present_illness",
        prompt=_t("When did it start?", "यह कब शुरू हुआ?"),
        easy_prompt=_t("Since when?", "कब से?"),
        help=_t("A rough idea is fine.", "अंदाज़ा भी ठीक है।"),
        options=(
            Option("Today", _t("Today", "आज")),
            Option("Yesterday", _t("Yesterday", "कल")),
            Option("2-3 days ago", _t("2–3 days ago", "2–3 दिन पहले")),
            Option("About a week ago", _t("About a week ago", "लगभग एक हफ़्ता पहले")),
            Option("Longer than a week", _t("Longer than a week", "एक हफ़्ते से ज़्यादा")),
        ),
    ),
    Question(
        id="e_severity",
        section="detail",
        kind=AnswerKind.SCALE,
        target="history_of_present_illness",
        options=_SCALE,
        prompt=_t(
            "How much is it troubling you, from 1 to 10?",
            "1 से 10 तक, यह आपको कितना परेशान कर रहा है?",
        ),
        easy_prompt=_t("How bad is it?", "कितनी तेज़ तकलीफ़ है?"),
        help=_t("1 is very mild, 10 is the worst.", "1 बहुत हल्का, 10 सबसे तेज़।"),
    ),
    Question(
        id="e_describe",
        section="detail",
        kind=AnswerKind.FREE_TEXT,
        target="history_of_present_illness",
        prompt=_t(
            "Can you describe it a little more?",
            "क्या आप इसे थोड़ा और बता सकते हैं?",
        ),
        help=_t(
            "For example where it is, what it feels like, or what makes it worse.",
            "जैसे यह कहाँ है, कैसा लगता है, या किससे बढ़ता है।",
        ),
    ),
    Question(
        id="e_associated",
        section="detail",
        kind=AnswerKind.MULTI_CHOICE,
        target="review_of_systems",
        prompt=_t("Is anything else happening as well?", "इसके साथ कुछ और भी हो रहा है?"),
        help=_t("Only choose what you actually feel.", "केवल वही चुनें जो आप महसूस करते हैं।"),
        options=(
            Option("Fever", _t("Fever", "बुखार")),
            Option("Vomiting", _t("Vomiting", "उल्टी")),
            Option("Loose motions", _t("Loose motions", "दस्त")),
            Option("Breathlessness", _t("Breathlessness", "सांस फूलना")),
            Option("Dizziness", _t("Dizziness", "चक्कर")),
            Option("Swelling", _t("Swelling", "सूजन")),
        ),
    ),
    Question(
        id="e_tried",
        section="detail",
        kind=AnswerKind.FREE_TEXT,
        target="history_of_present_illness",
        prompt=_t(
            "Have you taken anything for it?",
            "क्या आपने इसके लिए कुछ लिया है?",
        ),
        help=_t(
            "Any medicine or home remedy, even if it did not help.",
            "कोई दवा या घरेलू उपाय, चाहे उससे फ़र्क न पड़ा हो।",
        ),
    ),
    # --- What is new since last time ------------------------------------
    Question(
        id="e_meds_changed",
        section="changes",
        kind=AnswerKind.YES_NO,
        options=_YES_NO,
        prompt=_t(
            "Have your regular medicines changed since your last visit?",
            "पिछली बार से आपकी नियमित दवाइयाँ बदली हैं?",
        ),
        help=_t(
            "We already have your earlier list — only tell us what changed.",
            "आपकी पिछली सूची हमारे पास है — केवल बदलाव बताएं।",
        ),
    ),
    Question(
        id="e_meds_new",
        section="changes",
        kind=AnswerKind.LIST,
        target="current_medications",
        when=_said_yes("e_meds_changed"),
        prompt=_t("What has changed?", "क्या बदला है?"),
        help=_t(
            "A medicine you started, stopped, or now take differently.",
            "कोई दवा जो शुरू की, बंद की, या अब अलग तरह से लेते हैं।",
        ),
    ),
    Question(
        id="e_new_conditions",
        section="changes",
        kind=AnswerKind.YES_NO,
        options=_YES_NO,
        prompt=_t(
            "Has a doctor told you about any new condition since then?",
            "उसके बाद किसी डॉक्टर ने कोई नई बीमारी बताई है?",
        ),
        help=_t("Only something new.", "केवल कुछ नया।"),
    ),
    Question(
        id="e_new_conditions_detail",
        section="changes",
        kind=AnswerKind.LIST,
        target="past_medical_history",
        when=_said_yes("e_new_conditions"),
        prompt=_t("What was it?", "वह क्या था?"),
        help=_t("Add them one at a time.", "एक-एक जोड़ें।"),
    ),
    Question(
        id="e_anything_else",
        section="changes",
        kind=AnswerKind.FREE_TEXT,
        target="additional_information",
        prompt=_t(
            "Anything else you want the doctor to know today?",
            "आज कुछ और जो आप डॉक्टर को बताना चाहें?",
        ),
        help=_t("This is your space.", "यह जगह आपकी है।"),
    ),
)

QUESTION_BY_ID = {question.id: question for question in QUESTIONS}
TEMPLATED_IDS: set[str] = set()

# Free-text answers from these questions are what red-flag screening reads.
SCREENED_QUESTION_IDS = frozenset(
    {"e_complaint", "e_describe", "e_associated", "e_tried", "e_anything_else"}
)


class EncounterScript:
    """Satisfies `interview.engine.Script`, so the engine is reused as-is."""

    name = "encounter"

    @property
    def section_order(self) -> list[str]:
        return list(SECTION_ORDER)

    def sections_by_key(self) -> dict[str, Section]:
        return SECTION_BY_KEY

    def base_questions_for(self, section: str) -> list[Question]:
        return [q for q in QUESTIONS if q.section == section and q.id not in TEMPLATED_IDS]

    def question_by_id(self, question_id: str) -> Question | None:
        from app.modules.interview.questions import AI_FOLLOW_UP

        if question_id == AI_FOLLOW_UP.id:
            return AI_FOLLOW_UP
        return QUESTION_BY_ID.get(question_id)


ENCOUNTER_SCRIPT = EncounterScript()


# --- AYUSH questions, generated from the examination content --------------
# Built from `ayush/content.py` rather than restated here, so the standalone
# AYUSH screen and the in-visit questions can never diverge.


def _ayush_questions() -> tuple[Question, ...]:
    from app.modules.ayush.content import (
        AHARA_OPTIONS,
        ASHTASTHANA,
        DASHAVIDHA,
        LIFESTYLE_FACTORS,
        VIHARA_OPTIONS,
    )

    def single(prefix: str, section: str, factor: dict) -> Question:
        return Question(
            id=f"{prefix}{factor['key']}",
            section=section,
            kind=AnswerKind.SINGLE_CHOICE,
            # No `target`: these are not medical-profile facts. The encounter
            # service routes them into the AYUSH assessment instead.
            prompt=factor["prompt"],
            help=factor["help"],
            options=tuple(
                Option(option["value"], option["label"]) for option in factor["options"]
            ),
            allow_none=True,
        )

    generated: list[Question] = []
    for factor in DASHAVIDHA:
        generated.append(single("ay_dash_", "ayush_dashavidha", factor))
    for factor in ASHTASTHANA:
        generated.append(single("ay_ashta_", "ayush_ashtasthana", factor))
    for factor in LIFESTYLE_FACTORS:
        generated.append(single("ay_life_", "ayush_lifestyle", factor))

    generated.append(
        Question(
            id="ay_ahara",
            section="ayush_lifestyle",
            kind=AnswerKind.MULTI_CHOICE,
            prompt=_t("Which of these describe your diet?", "इनमें से कौन आपके आहार को बताता है?"),
            help=_t("Choose as many as apply.", "जितने लागू हों चुनें।"),
            options=tuple(Option(o["value"], o["label"]) for o in AHARA_OPTIONS),
        )
    )
    generated.append(
        Question(
            id="ay_vihara",
            section="ayush_lifestyle",
            kind=AnswerKind.MULTI_CHOICE,
            prompt=_t("And your daily routine?", "और आपकी दिनचर्या?"),
            help=_t("Choose as many as apply.", "जितने लागू हों चुनें।"),
            options=tuple(Option(o["value"], o["label"]) for o in VIHARA_OPTIONS),
        )
    )
    return tuple(generated)


AYUSH_QUESTIONS = _ayush_questions()
QUESTIONS = (*QUESTIONS, *AYUSH_QUESTIONS)
QUESTION_BY_ID = {question.id: question for question in QUESTIONS}

# Which AYUSH assessment field each question id writes to.
AYUSH_FIELD_BY_PREFIX = {
    "ay_dash_": "dashavidha",
    "ay_ashta_": "ashtasthana",
    "ay_life_": "lifestyle",
}


def ayush_target(question_id: str) -> tuple[str, str] | None:
    """@returns (assessment field, factor key) for an AYUSH question."""
    for prefix, field in AYUSH_FIELD_BY_PREFIX.items():
        if question_id.startswith(prefix):
            return field, question_id[len(prefix) :]
    if question_id == "ay_ahara":
        return "ahara", ""
    if question_id == "ay_vihara":
        return "vihara", ""
    return None


def core_question_count() -> int:
    """Questions an allopathic visit can be asked (the care-system question
    plus today's concern), for comparison with the AYUSH total."""
    return len([q for q in QUESTIONS if not q.id.startswith("ay_")])
