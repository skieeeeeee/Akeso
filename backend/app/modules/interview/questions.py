"""The interview script.

Sections and questions are DATA, not code paths. The engine walks this list,
which is what keeps the workflow under application control: the AI can suggest
a follow-up, but it can never invent a section, skip consent or reorder the
interview.

`target` is the medical-profile section an answer is written to, so the profile
stays the single source of truth for clinical facts and the interview owns only
navigation state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from app.shared.enums import AnswerKind, Language
from app.shared.i18n import Localised, localise, t as _t





@dataclass(frozen=True, slots=True)
class Option:
    value: str
    label: Localised
    icon: str | None = None


@dataclass(frozen=True, slots=True)
class Section:
    key: str
    title: Localised
    intro: Localised
    icon: str
    # AYUSH is only walked when the patient opts in.
    optional: bool = False


SECTIONS: tuple[Section, ...] = (
    Section(
        key="presenting",
        title=_t("Why you are here", "आप क्यों आए हैं"),
        intro=_t(
            "First, tell us what brings you in today.",
            "पहले बताएं कि आज आप किस कारण आए हैं।",
        ),
        icon="stethoscope",
    ),
    Section(
        key="conditions",
        title=_t("Ongoing conditions", "चल रही बीमारियाँ"),
        intro=_t(
            "Now a few questions about long-term health conditions.",
            "अब कुछ सवाल पुरानी बीमारियों के बारे में।",
        ),
        icon="activity",
    ),
    Section(
        key="surgeries",
        title=_t("Operations", "ऑपरेशन"),
        intro=_t("Have you ever had an operation?", "क्या आपका कभी ऑपरेशन हुआ है?"),
        icon="scissors",
    ),
    Section(
        key="medications",
        title=_t("Medicines", "दवाइयाँ"),
        intro=_t(
            "Let us record the medicines you take.",
            "आइए आपकी दवाइयाँ दर्ज करें।",
        ),
        icon="pill",
    ),
    Section(
        key="allergies",
        title=_t("Allergies", "एलर्जी"),
        intro=_t(
            "This one matters a lot for your safety.",
            "यह आपकी सुरक्षा के लिए बहुत ज़रूरी है।",
        ),
        icon="alert-triangle",
    ),
    Section(
        key="family",
        title=_t("Family health", "पारिवारिक स्वास्थ्य"),
        intro=_t(
            "Some illnesses run in families.",
            "कुछ बीमारियाँ परिवार में चलती हैं।",
        ),
        icon="users",
    ),
    Section(
        key="personal",
        title=_t("Daily life", "दैनिक जीवन"),
        intro=_t(
            "A few questions about your habits and routine.",
            "आपकी आदतों और दिनचर्या के बारे में कुछ सवाल।",
        ),
        icon="activity",
    ),
    Section(
        key="investigations",
        title=_t("Earlier tests", "पिछली जाँचें"),
        intro=_t(
            "Any tests you have had done recently.",
            "हाल में कराई गई कोई जाँच।",
        ),
        icon="flask",
    ),
    Section(
        key="review_of_systems",
        title=_t("Anything else you feel", "कुछ और जो महसूस हो"),
        intro=_t(
            "A quick check for other symptoms.",
            "अन्य लक्षणों की तेज़ जाँच।",
        ),
        icon="message",
    ),
    Section(
        key="ayush",
        title=_t("Ayurveda assessment", "आयुर्वेद मूल्यांकन"),
        intro=_t(
            "Optional questions used in Ayurvedic practice.",
            "आयुर्वेदिक चिकित्सा में उपयोग होने वाले वैकल्पिक सवाल।",
        ),
        icon="book",
        optional=True,
    ),
)

SECTION_BY_KEY = {section.key: section for section in SECTIONS}
SECTION_ORDER = [section.key for section in SECTIONS]


@dataclass(frozen=True, slots=True)
class Question:
    id: str
    section: str
    kind: AnswerKind
    prompt: Localised
    help: Localised
    # Which medical-profile section the answer is written to. None = navigation
    # only (e.g. the yes/no gate before a list question).
    target: str | None = None
    easy_prompt: Localised | None = None
    options: tuple[Option, ...] = ()
    suggestions: tuple[Localised, ...] = ()
    allow_none: bool = True
    required: bool = False
    # Ask only when this holds. `answers` maps question id -> stored answer.
    when: Callable[[dict[str, str]], bool] | None = field(default=None, compare=False)
    # For each item recorded by this question, queue these templated questions.
    per_item: tuple[str, ...] = ()


def text_for(question: Question, language: Language | str, easy: bool) -> str:
    if easy and question.easy_prompt:
        return localise(question.easy_prompt, language)
    return localise(question.prompt, language)


# --- Reusable option sets --------------------------------------------------

YES_NO: tuple[Option, ...] = (
    Option("yes", _t("Yes", "हाँ"), "check"),
    Option("no", _t("No", "नहीं"), "minus"),
)

_SEVERITY: tuple[Option, ...] = tuple(
    Option(str(n), _t(str(n), str(n))) for n in range(1, 11)
)


def _said_yes(question_id: str) -> Callable[[dict[str, str]], bool]:
    return lambda answers: answers.get(question_id, "").strip().lower() == "yes"


# --- The question bank ----------------------------------------------------
# Templated per-item questions live here too; the engine substitutes {item}.

QUESTIONS: tuple[Question, ...] = (
    # ---- Presenting problem ----------------------------------------------
    Question(
        id="q_chief_complaint",
        section="presenting",
        kind=AnswerKind.FREE_TEXT,
        target="chief_complaint",
        required=True,
        allow_none=False,
        prompt=_t(
            "What problem brings you in today?",
            "आज आप किस तकलीफ़ के लिए आए हैं?",
        ),
        easy_prompt=_t("What is troubling you?", "आपको क्या तकलीफ़ है?"),
        help=_t(
            "Describe it in your own words. You can speak instead of typing.",
            "अपने शब्दों में बताएं। आप टाइप करने के बजाय बोल भी सकते हैं।",
        ),
        suggestions=(
            _t("Chest pain", "सीने में दर्द"),
            _t("Fever", "बुखार"),
            _t("Headache", "सिर दर्द"),
            _t("Stomach pain", "पेट में दर्द"),
            _t("Cough", "खांसी"),
            _t("Only here for a check-up", "केवल जाँच के लिए आया/आई हूँ"),
        ),
    ),
    Question(
        id="q_duration",
        section="presenting",
        kind=AnswerKind.SINGLE_CHOICE,
        target="history_of_present_illness",
        prompt=_t("How long have you had this?", "यह कब से है?"),
        easy_prompt=_t("Since when?", "कब से?"),
        help=_t("A rough idea is fine.", "अंदाज़ा भी ठीक है।"),
        options=(
            Option("Started today", _t("Started today", "आज से")),
            Option("2-3 days", _t("2–3 days", "2–3 दिन")),
            Option("About a week", _t("About a week", "लगभग एक हफ़्ता")),
            Option("A few weeks", _t("A few weeks", "कुछ हफ़्ते")),
            Option("More than a month", _t("More than a month", "एक महीने से ज़्यादा")),
        ),
    ),
    Question(
        id="q_severity",
        section="presenting",
        kind=AnswerKind.SCALE,
        target="history_of_present_illness",
        prompt=_t(
            "How much does it trouble you, from 1 to 10?",
            "1 से 10 तक, यह आपको कितना परेशान करता है?",
        ),
        easy_prompt=_t("How bad is it?", "कितनी तेज़ तकलीफ़ है?"),
        help=_t("1 is very mild, 10 is the worst.", "1 बहुत हल्का, 10 सबसे तेज़।"),
        options=_SEVERITY,
    ),
    Question(
        id="q_hpi_detail",
        section="presenting",
        kind=AnswerKind.FREE_TEXT,
        target="history_of_present_illness",
        prompt=_t(
            "Is there anything that makes it better or worse?",
            "क्या कुछ ऐसा है जिससे यह बढ़ता या कम होता है?",
        ),
        help=_t(
            "For example rest, food, walking, or a medicine you took.",
            "जैसे आराम, खाना, चलना, या कोई दवा जो आपने ली।",
        ),
    ),
    # ---- Ongoing conditions ----------------------------------------------
    Question(
        id="q_has_conditions",
        section="conditions",
        kind=AnswerKind.YES_NO,
        options=YES_NO,
        prompt=_t(
            "Has a doctor told you that you have a long-term illness?",
            "क्या किसी डॉक्टर ने बताया है कि आपको कोई पुरानी बीमारी है?",
        ),
        easy_prompt=_t("Any old illness?", "कोई पुरानी बीमारी?"),
        help=_t(
            "Such as diabetes, blood pressure or asthma.",
            "जैसे मधुमेह, रक्तचाप या दमा।",
        ),
    ),
    Question(
        id="q_conditions",
        section="conditions",
        kind=AnswerKind.LIST,
        target="past_medical_history",
        when=_said_yes("q_has_conditions"),
        # Each condition triggers the medicine follow-ups below.
        per_item=("q_condition_medicine", "q_condition_medicine_name"),
        prompt=_t("Which ones?", "कौन सी?"),
        easy_prompt=_t("Which illness?", "कौन सी बीमारी?"),
        help=_t(
            "Add them one at a time. Tap a common answer or say it aloud.",
            "एक-एक जोड़ें। कोई सामान्य जवाब छुएं या बोलकर बताएं।",
        ),
        suggestions=(
            _t("Diabetes", "मधुमेह"),
            _t("High blood pressure", "उच्च रक्तचाप"),
            _t("Asthma", "दमा"),
            _t("Thyroid problem", "थायरॉइड"),
            _t("Heart disease", "हृदय रोग"),
            _t("Tuberculosis", "तपेदिक"),
        ),
    ),
    # Templated: the engine fills {item} with each recorded condition. This is
    # the spec's worked example — "I have diabetes" -> medicine -> which one.
    Question(
        id="q_condition_medicine",
        section="conditions",
        kind=AnswerKind.YES_NO,
        options=YES_NO,
        prompt=_t(
            "Are you currently taking medicine for {item}?",
            "क्या आप अभी {item} के लिए दवा ले रहे हैं?",
        ),
        help=_t("Yes or no is enough.", "हाँ या नहीं ही पर्याप्त है।"),
    ),
    Question(
        id="q_condition_medicine_name",
        section="conditions",
        kind=AnswerKind.LIST,
        target="current_medications",
        when=_said_yes("q_condition_medicine"),
        prompt=_t(
            "Do you remember the name of the medicine for {item}?",
            "क्या आपको {item} की दवा का नाम याद है?",
        ),
        help=_t(
            "If you are not sure, you can skip this or upload the prescription later.",
            "यदि याद न हो तो इसे छोड़ें या बाद में पर्चा अपलोड करें।",
        ),
    ),
    # ---- Surgeries --------------------------------------------------------
    Question(
        id="q_has_surgery",
        section="surgeries",
        kind=AnswerKind.YES_NO,
        options=YES_NO,
        prompt=_t("Have you ever had an operation?", "क्या आपका कभी ऑपरेशन हुआ है?"),
        help=_t("Any operation, however long ago.", "कोई भी ऑपरेशन, कितना भी पुराना।"),
    ),
    Question(
        id="q_surgeries",
        section="surgeries",
        kind=AnswerKind.LIST,
        target="surgical_history",
        when=_said_yes("q_has_surgery"),
        prompt=_t("What operation, and roughly when?", "कौन सा ऑपरेशन, और लगभग कब?"),
        help=_t(
            "For example: gallbladder removed, 2019.",
            "जैसे: पित्ताशय निकाला गया, 2019।",
        ),
    ),
    # ---- Medications ------------------------------------------------------
    Question(
        id="q_medications",
        section="medications",
        kind=AnswerKind.LIST,
        target="current_medications",
        prompt=_t(
            "Which medicines do you take regularly?",
            "आप नियमित रूप से कौन सी दवाइयाँ लेते हैं?",
        ),
        easy_prompt=_t("Any daily medicine?", "रोज़ कोई दवा?"),
        help=_t(
            "Include tablets, insulin, inhalers and drops.",
            "गोलियाँ, इंसुलिन, इनहेलर और ड्रॉप्स शामिल करें।",
        ),
    ),
    Question(
        id="q_drug_history",
        section="medications",
        kind=AnswerKind.FREE_TEXT,
        target="drug_history",
        prompt=_t(
            "Has any medicine ever caused you a problem?",
            "क्या किसी दवा से आपको कभी दिक्कत हुई है?",
        ),
        help=_t(
            "For example it upset your stomach, or you had to stop it.",
            "जैसे पेट खराब हुआ, या आपको बंद करनी पड़ी।",
        ),
    ),
    # ---- Allergies --------------------------------------------------------
    Question(
        id="q_allergies",
        section="allergies",
        kind=AnswerKind.LIST,
        target="allergies",
        required=True,
        prompt=_t(
            "Are you allergic to any medicine or food?",
            "किसी दवा या खाने से एलर्जी है?",
        ),
        easy_prompt=_t("Any allergy?", "कोई एलर्जी?"),
        help=_t(
            "Tell us even if you are unsure — it keeps you safe.",
            "यदि पक्का न हो तो भी बताएं — यह आपकी सुरक्षा के लिए है।",
        ),
        suggestions=(
            _t("No known allergies", "कोई ज्ञात एलर्जी नहीं"),
            _t("Penicillin", "पेनिसिलिन"),
            _t("Sulfa drugs", "सल्फा दवाएँ"),
            _t("Aspirin", "एस्पिरिन"),
            _t("Dust", "धूल"),
        ),
    ),
    # ---- Family -----------------------------------------------------------
    Question(
        id="q_family",
        section="family",
        kind=AnswerKind.LIST,
        target="family_history",
        prompt=_t(
            "Does any illness run in your close family?",
            "आपके नज़दीकी परिवार में कोई बीमारी चलती है?",
        ),
        easy_prompt=_t("Any illness in the family?", "परिवार में कोई बीमारी?"),
        help=_t(
            "Parents, brothers, sisters or children.",
            "माता-पिता, भाई, बहन या बच्चे।",
        ),
        suggestions=(
            _t("Diabetes", "मधुमेह"),
            _t("High blood pressure", "उच्च रक्तचाप"),
            _t("Heart disease", "हृदय रोग"),
            _t("Cancer", "कैंसर"),
        ),
    ),
    # ---- Personal ---------------------------------------------------------
    Question(
        id="q_personal",
        section="personal",
        kind=AnswerKind.MULTI_CHOICE,
        target="personal_history",
        prompt=_t(
            "Which of these apply to you?",
            "इनमें से कौन आप पर लागू होता है?",
        ),
        help=_t("Choose as many as you like.", "जितने चाहें चुनें।"),
        options=(
            Option("Non-smoker", _t("I do not smoke", "मैं धूम्रपान नहीं करता/करती")),
            Option("Smoker", _t("I smoke", "मैं धूम्रपान करता/करती हूँ")),
            Option("No alcohol", _t("I do not drink alcohol", "मैं शराब नहीं पीता/पीती")),
            Option("Drinks alcohol", _t("I drink alcohol", "मैं शराब पीता/पीती हूँ")),
            Option("Vegetarian diet", _t("Vegetarian diet", "शाकाहारी भोजन")),
            Option("Exercises regularly", _t("I exercise regularly", "मैं नियमित व्यायाम करता/करती हूँ")),
        ),
    ),
    Question(
        id="q_occupation",
        section="personal",
        kind=AnswerKind.FREE_TEXT,
        target="personal_history",
        prompt=_t("What work do you do?", "आप क्या काम करते हैं?"),
        help=_t(
            "Some jobs affect health, so this can be useful.",
            "कुछ काम स्वास्थ्य पर असर डालते हैं, इसलिए यह उपयोगी हो सकता है।",
        ),
    ),
    # ---- Investigations ---------------------------------------------------
    Question(
        id="q_has_investigations",
        section="investigations",
        kind=AnswerKind.YES_NO,
        options=YES_NO,
        prompt=_t(
            "Have you had any blood test or scan recently?",
            "क्या हाल में आपका कोई खून की जाँच या स्कैन हुआ है?",
        ),
        help=_t("In the last year or so.", "लगभग पिछले एक साल में।"),
    ),
    Question(
        id="q_investigations",
        section="investigations",
        kind=AnswerKind.LIST,
        target="previous_investigations",
        when=_said_yes("q_has_investigations"),
        prompt=_t(
            "Which test, and what did it show?",
            "कौन सी जाँच, और उसमें क्या आया?",
        ),
        help=_t(
            "If you have the report, you can upload it in the next step instead.",
            "यदि रिपोर्ट है तो अगले चरण में अपलोड कर सकते हैं।",
        ),
    ),
    # ---- Review of systems ------------------------------------------------
    Question(
        id="q_review_of_systems",
        section="review_of_systems",
        kind=AnswerKind.MULTI_CHOICE,
        target="review_of_systems",
        prompt=_t(
            "Are you also feeling any of these?",
            "क्या आपको इनमें से कुछ और भी महसूस हो रहा है?",
        ),
        help=_t(
            "Only choose what you actually feel.",
            "केवल वही चुनें जो आप वाकई महसूस करते हैं।",
        ),
        options=(
            Option("Weight loss", _t("Losing weight", "वज़न घट रहा है")),
            Option("Tiredness", _t("Very tired", "बहुत थकान")),
            Option("Breathlessness", _t("Short of breath", "सांस फूलना")),
            Option("Fever", _t("Fever", "बुखार")),
            Option("Swelling", _t("Swelling", "सूजन")),
            Option("Poor sleep", _t("Not sleeping well", "नींद ठीक नहीं")),
        ),
    ),
    Question(
        id="q_anything_else",
        section="review_of_systems",
        kind=AnswerKind.FREE_TEXT,
        target="additional_information",
        prompt=_t(
            "Anything else you would like your doctor to know?",
            "कुछ और जो आप अपने डॉक्टर को बताना चाहें?",
        ),
        help=_t("This is your space.", "यह जगह आपकी है।"),
    ),
)

# Generic carrier for an AI-suggested follow-up. The suggested text and
# target travel on the queue entry; this question supplies the shape and the
# validation rules, so a model can never introduce a new answer kind.
AI_FOLLOW_UP = Question(
    id="q_ai_follow_up",
    section="presenting",
    kind=AnswerKind.FREE_TEXT,
    prompt=_t("Could you tell us a little more?", "क्या आप थोड़ा और बता सकते हैं?"),
    help=_t(
        "This question was suggested from what you just said. You can skip it.",
        "यह सवाल आपके अभी दिए जवाब से सुझाया गया है। आप इसे छोड़ सकते हैं।",
    ),
)

QUESTIONS_ALL: tuple[Question, ...] = (*QUESTIONS, AI_FOLLOW_UP)
QUESTION_BY_ID = {question.id: question for question in QUESTIONS_ALL}

# Questions used only as per-item templates are never scheduled directly.
TEMPLATED_IDS = {
    template for question in QUESTIONS for template in question.per_item
}


def question_by_id(question_id: str) -> Question | None:
    return QUESTION_BY_ID.get(question_id)


def base_questions_for(section: str) -> list[Question]:
    return [
        question
        for question in QUESTIONS
        if question.section == section and question.id not in TEMPLATED_IDS
    ]
