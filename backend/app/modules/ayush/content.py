"""AYUSH question content.

Dashavidha Pariksha is a clinician's ten-fold examination; the wording here is
the patient-answerable form of each factor, so a layperson can respond without
knowing the Sanskrit terms. The term is still shown, because patients at an
AYUSH facility often recognise it.
"""

from __future__ import annotations

from typing import Any

from app.shared.enums import AyushAshtasthana, AyushPariksha
from app.shared.i18n import Localised, localise, t as _t




def _opts(*pairs: tuple[str, str, str]) -> list[dict[str, Any]]:
    return [{"value": value, "label": _t(en, hi)} for value, en, hi in pairs]


DASHAVIDHA: list[dict[str, Any]] = [
    {
        "key": AyushPariksha.PRAKRITI.value,
        "term": _t("Prakriti", "प्रकृति"),
        "prompt": _t("Which best describes your natural build and temperament?",
                     "आपकी स्वाभाविक बनावट और स्वभाव को कौन सबसे ठीक बताता है?"),
        "help": _t("Your lifelong tendency, not how you feel today.",
                   "आपकी जीवनभर की प्रवृत्ति, आज की स्थिति नहीं।"),
        "options": _opts(
            ("vata", "Thin build, quick and restless", "पतली बनावट, तेज़ और चंचल"),
            ("pitta", "Medium build, sharp and warm", "मध्यम बनावट, तीक्ष्ण और गर्म"),
            ("kapha", "Heavier build, calm and steady", "भारी बनावट, शांत और स्थिर"),
            ("mixed", "A mixture", "मिश्रित"),
            ("unsure", "I am not sure", "मुझे पता नहीं"),
        ),
    },
    {
        "key": AyushPariksha.VIKRITI.value,
        "term": _t("Vikriti", "विकृति"),
        "prompt": _t("How do you feel compared with your usual self?",
                     "अपनी सामान्य स्थिति की तुलना में आप कैसा महसूस करते हैं?"),
        "help": _t("Your current state, today.", "आपकी आज की वर्तमान स्थिति।"),
        "options": _opts(
            ("normal", "Same as usual", "सामान्य जैसा"),
            ("dry_restless", "Dry, gassy or restless", "रूखापन, गैस या बेचैनी"),
            ("hot_acidic", "Hot, acidic or irritable", "गर्मी, अम्लता या चिड़चिड़ापन"),
            ("heavy_sluggish", "Heavy, congested or sluggish", "भारीपन, जकड़न या सुस्ती"),
        ),
    },
    {
        "key": AyushPariksha.SARA.value,
        "term": _t("Sara", "सार"),
        "prompt": _t("How would you describe your overall vitality?",
                     "आप अपनी कुल जीवनशक्ति को कैसे बताएंगे?"),
        "help": _t("How strong and resilient you generally feel.",
                   "आप सामान्यतः कितना मज़बूत और सहनशील महसूस करते हैं।"),
        "options": _opts(
            ("uttama", "Strong and resilient", "मज़बूत और सहनशील"),
            ("madhyama", "Average", "औसत"),
            ("avara", "Easily tired or weak", "जल्दी थकान या कमज़ोरी"),
        ),
    },
    {
        "key": AyushPariksha.SAMHANANA.value,
        "term": _t("Samhanana", "संहनन"),
        "prompt": _t("How is your body build?", "आपके शरीर की बनावट कैसी है?"),
        "help": _t("Muscle and frame, in your own view.", "मांसपेशी और ढांचा, आपकी दृष्टि से।"),
        "options": _opts(
            ("well_built", "Well built", "सुगठित"),
            ("moderate", "Moderate", "मध्यम"),
            ("poorly_built", "Thin or weak", "पतला या कमज़ोर"),
        ),
    },
    {
        "key": AyushPariksha.PRAMANA.value,
        "term": _t("Pramana", "प्रमाण"),
        "prompt": _t("How would you describe your height and weight together?",
                     "अपनी लंबाई और वज़न को साथ में कैसे बताएंगे?"),
        "help": _t("Roughly proportionate, or not.", "लगभग संतुलित, या नहीं।"),
        "options": _opts(
            ("proportionate", "Proportionate", "संतुलित"),
            ("underweight", "Underweight for my height", "लंबाई के हिसाब से कम वज़न"),
            ("overweight", "Overweight for my height", "लंबाई के हिसाब से अधिक वज़न"),
        ),
    },
    {
        "key": AyushPariksha.SATMYA.value,
        "term": _t("Satmya", "सात्म्य"),
        "prompt": _t("Which foods or conditions suit you well?",
                     "कौन से भोजन या परिस्थितियाँ आपको अनुकूल लगती हैं?"),
        "help": _t("What you tolerate easily.", "जो आप आसानी से सहन कर लेते हैं।"),
        "options": _opts(
            ("all", "Almost everything suits me", "लगभग सब कुछ अनुकूल है"),
            ("selective", "Only certain foods suit me", "केवल कुछ भोजन अनुकूल हैं"),
            ("sensitive", "Many things upset me", "कई चीज़ें परेशान करती हैं"),
        ),
    },
    {
        "key": AyushPariksha.SATTVA.value,
        "term": _t("Sattva", "सत्त्व"),
        "prompt": _t("How do you usually handle stress?",
                     "आप सामान्यतः तनाव को कैसे संभालते हैं?"),
        "help": _t("Your mental steadiness.", "आपकी मानसिक स्थिरता।"),
        "options": _opts(
            ("strong", "I stay steady", "मैं स्थिर रहता/रहती हूँ"),
            ("moderate", "It depends", "यह स्थिति पर निर्भर है"),
            ("sensitive", "I get upset easily", "मैं जल्दी परेशान हो जाता/जाती हूँ"),
        ),
    },
    {
        "key": AyushPariksha.AHARA_SHAKTI.value,
        "term": _t("Ahara Shakti", "आहार शक्ति"),
        "prompt": _t("How is your appetite and digestion?",
                     "आपकी भूख और पाचन कैसा है?"),
        "help": _t("How much you can eat and digest comfortably.",
                   "आप कितना खा और आराम से पचा सकते हैं।"),
        "options": _opts(
            ("strong", "Good appetite, digests well", "अच्छी भूख, ठीक पचता है"),
            ("moderate", "Average", "औसत"),
            ("weak", "Poor appetite or heaviness after food", "कम भूख या खाने के बाद भारीपन"),
        ),
    },
    {
        "key": AyushPariksha.VYAYAMA_SHAKTI.value,
        "term": _t("Vyayama Shakti", "व्यायाम शक्ति"),
        "prompt": _t("How much physical exertion can you manage?",
                     "आप कितना शारीरिक परिश्रम कर सकते हैं?"),
        "help": _t("Before you need to rest.", "आराम की ज़रूरत पड़ने से पहले।"),
        "options": _opts(
            ("high", "A lot", "बहुत"),
            ("moderate", "A moderate amount", "मध्यम"),
            ("low", "Very little", "बहुत कम"),
        ),
    },
    {
        "key": AyushPariksha.VAYA.value,
        "term": _t("Vaya", "वय"),
        "prompt": _t("Which life stage are you in?", "आप किस आयु अवस्था में हैं?"),
        "help": _t("Usually filled in from your date of birth.",
                   "सामान्यतः आपकी जन्म तिथि से भरा जाता है।"),
        "options": _opts(
            ("bala", "Childhood or youth (under 30)", "बाल्य या तरुण (30 से कम)"),
            ("madhya", "Middle years (30–60)", "मध्य आयु (30–60)"),
            ("vriddha", "Older years (over 60)", "वृद्ध आयु (60 से अधिक)"),
        ),
    },
]

# --- Ashtasthana Pariksha (eight-fold examination) -----------------------
# Normally a clinician examines these directly. Phrased here as the
# patient-answerable form, so a self-report can be recorded before the
# consultation and the practitioner confirms it at the couch.

ASHTASTHANA: list[dict[str, Any]] = [
    {
        "key": AyushAshtasthana.NADI.value,
        "term": _t("Nadi", "नाड़ी"),
        "prompt": _t("How does your pulse or heartbeat usually feel?",
                     "आपकी नाड़ी या दिल की धड़कन आमतौर पर कैसी लगती है?"),
        "help": _t("Your own sense of it — a practitioner will check properly.",
                   "आपका स्वयं का अनुभव — वैद्य इसे ठीक से देखेंगे।"),
        "options": _opts(
            ("normal", "Normal and steady", "सामान्य और स्थिर"),
            ("fast", "Often fast", "अक्सर तेज़"),
            ("slow", "Often slow", "अक्सर धीमी"),
            ("irregular", "Sometimes irregular", "कभी-कभी अनियमित"),
            ("unsure", "I have not noticed", "मैंने ध्यान नहीं दिया"),
        ),
    },
    {
        "key": AyushAshtasthana.MUTRA.value,
        "term": _t("Mutra", "मूत्र"),
        "prompt": _t("How is your urine?", "आपका पेशाब कैसा है?"),
        "help": _t("Colour, quantity and how often.", "रंग, मात्रा और कितनी बार।"),
        "options": _opts(
            ("normal", "Normal", "सामान्य"),
            ("dark_scanty", "Dark or less than usual", "गहरा या कम"),
            ("frequent", "More often than usual", "आमतौर से ज़्यादा बार"),
            ("burning", "Burning or discomfort", "जलन या तकलीफ़"),
        ),
    },
    {
        "key": AyushAshtasthana.MALA.value,
        "term": _t("Mala", "मल"),
        "prompt": _t("How are your bowel movements?", "आपका मल त्याग कैसा है?"),
        "help": _t("Regularity and consistency.", "नियमितता और स्थिति।"),
        "options": _opts(
            ("regular", "Regular and easy", "नियमित और सहज"),
            ("constipated", "Hard or difficult", "कठोर या कठिनाई से"),
            ("loose", "Loose or frequent", "पतला या बार-बार"),
            ("irregular", "Irregular", "अनियमित"),
        ),
    },
    {
        "key": AyushAshtasthana.JIHVA.value,
        "term": _t("Jihva", "जिह्वा"),
        "prompt": _t("How does your tongue look and feel?", "आपकी जीभ कैसी दिखती और लगती है?"),
        "help": _t("Coating, dryness or taste in the mouth.",
                   "परत, सूखापन या मुँह का स्वाद।"),
        "options": _opts(
            ("clean", "Clean and moist", "साफ़ और नम"),
            ("coated", "Coated or white", "परत या सफ़ेदी"),
            ("dry", "Dry", "सूखी"),
            ("bad_taste", "Bad or altered taste", "स्वाद ख़राब या बदला हुआ"),
        ),
    },
    {
        "key": AyushAshtasthana.SHABDA.value,
        "term": _t("Shabda", "शब्द"),
        "prompt": _t("How is your voice at present?", "आपकी आवाज़ अभी कैसी है?"),
        "help": _t("Strength and clarity when you speak.",
                   "बोलते समय बल और स्पष्टता।"),
        "options": _opts(
            ("clear", "Clear and normal", "स्पष्ट और सामान्य"),
            ("weak", "Weak or low", "कमज़ोर या धीमी"),
            ("hoarse", "Hoarse", "भारी या बैठी हुई"),
            ("breathless", "Breathless when speaking", "बोलते समय सांस फूलती है"),
        ),
    },
    {
        "key": AyushAshtasthana.SPARSHA.value,
        "term": _t("Sparsha", "स्पर्श"),
        "prompt": _t("How does your skin feel to touch?", "छूने पर आपकी त्वचा कैसी लगती है?"),
        "help": _t("Temperature, dryness or sweating.", "तापमान, रूखापन या पसीना।"),
        "options": _opts(
            ("normal", "Normal", "सामान्य"),
            ("hot", "Warm or feverish", "गर्म या बुख़ार जैसी"),
            ("cold", "Cold", "ठंडी"),
            ("dry", "Dry or rough", "रूखी या खुरदरी"),
            ("sweaty", "Sweating a lot", "बहुत पसीना"),
        ),
    },
    {
        "key": AyushAshtasthana.DRIK.value,
        "term": _t("Drik", "दृक्"),
        "prompt": _t("How are your eyes and vision?", "आपकी आँखें और दृष्टि कैसी हैं?"),
        "help": _t("Only what you notice yourself.", "केवल जो आप स्वयं महसूस करते हैं।"),
        "options": _opts(
            ("normal", "Normal", "सामान्य"),
            ("red_burning", "Red or burning", "लाल या जलन"),
            ("watery", "Watery", "पानी आना"),
            ("blurred", "Blurred", "धुंधला"),
            ("dry", "Dry", "सूखी"),
        ),
    },
    {
        "key": AyushAshtasthana.AKRITI.value,
        "term": _t("Akriti", "आकृति"),
        "prompt": _t("How would you describe your overall appearance now?",
                     "अभी अपनी कुल शारीरिक स्थिति को कैसे बताएंगे?"),
        "help": _t("How you look and feel compared with your usual self.",
                   "अपनी सामान्य स्थिति की तुलना में आप कैसे दिखते और महसूस करते हैं।"),
        "options": _opts(
            ("normal", "Same as usual", "सामान्य जैसा"),
            ("tired", "Tired or drawn", "थका या मुरझाया"),
            ("swollen", "Puffy or swollen", "फूला या सूजा"),
            ("lost_weight", "Thinner than before", "पहले से पतला"),
        ),
    },
]

# --- Agni / Koshtha, Nidra, Manas ----------------------------------------

LIFESTYLE_FACTORS: list[dict[str, Any]] = [
    {
        "key": "agni",
        "term": _t("Agni", "अग्नि"),
        "prompt": _t("How well do you digest your food?", "आप अपना भोजन कितना अच्छा पचाते हैं?"),
        "help": _t("Whether food feels heavy, or digests comfortably.",
                   "भोजन भारी लगता है या आराम से पचता है।"),
        "options": _opts(
            ("strong", "Digests easily", "आसानी से पचता है"),
            ("variable", "Varies from day to day", "दिन-प्रतिदिन बदलता है"),
            ("weak", "Often heavy or slow", "अक्सर भारी या धीमा"),
            ("burning", "Burning or acidity", "जलन या अम्लता"),
        ),
    },
    {
        "key": "koshtha",
        "term": _t("Koshtha", "कोष्ठ"),
        "prompt": _t("How does your gut normally behave?", "आपका पेट आमतौर पर कैसा रहता है?"),
        "help": _t("Your usual tendency, not just today.",
                   "आपकी सामान्य प्रवृत्ति, केवल आज की नहीं।"),
        "options": _opts(
            ("mridu", "Moves easily, sometimes loose", "आसानी से चलता है, कभी पतला"),
            ("madhyama", "Regular", "नियमित"),
            ("krura", "Tends to be constipated", "कब्ज़ की प्रवृत्ति"),
        ),
    },
    {
        "key": "nidra",
        "term": _t("Nidra", "निद्रा"),
        "prompt": _t("How is your sleep?", "आपकी नींद कैसी है?"),
        "help": _t("Falling asleep, staying asleep, and feeling rested.",
                   "नींद आना, बनी रहना, और तरोताज़ा महसूस होना।"),
        "options": _opts(
            ("sound", "Sound and refreshing", "गहरी और तरोताज़ा"),
            ("difficulty_falling", "Hard to fall asleep", "नींद आने में कठिनाई"),
            ("broken", "Wakes during the night", "रात में नींद टूटती है"),
            ("excessive", "Sleeping more than usual", "आमतौर से ज़्यादा नींद"),
            ("unrefreshed", "Wake up tired", "उठने पर थकान"),
        ),
    },
    {
        "key": "manas",
        "term": _t("Manas", "मनस्"),
        "prompt": _t("How has your mind felt lately?", "हाल में आपका मन कैसा रहा है?"),
        "help": _t(
            "Only if you wish to say. This is recorded for your practitioner, not assessed here.",
            "केवल यदि आप बताना चाहें। यह आपके वैद्य के लिए दर्ज होता है, यहाँ आँका नहीं जाता।",
        ),
        "options": _opts(
            ("calm", "Calm and steady", "शांत और स्थिर"),
            ("worried", "Worried or restless", "चिंतित या बेचैन"),
            ("irritable", "Irritable", "चिड़चिड़ा"),
            ("low", "Low or heavy", "उदास या भारी"),
            ("prefer_not", "I would rather not say", "मैं बताना नहीं चाहता/चाहती"),
        ),
    },
]

AHARA_OPTIONS: list[dict[str, Any]] = _opts(
    ("vegetarian", "Vegetarian", "शाकाहारी"),
    ("non_vegetarian", "Non-vegetarian", "मांसाहारी"),
    ("mostly_home_cooked", "Mostly home-cooked food", "अधिकतर घर का बना भोजन"),
    ("frequent_outside_food", "Often eat outside food", "अक्सर बाहर का खाना"),
    ("irregular_meals", "Meal times are irregular", "भोजन का समय अनियमित"),
    ("spicy_food", "Prefer spicy food", "मसालेदार भोजन पसंद"),
    ("frequent_tea_coffee", "Frequent tea or coffee", "बार-बार चाय या कॉफ़ी"),
    ("low_water", "I drink little water", "मैं कम पानी पीता/पीती हूँ"),
)

VIHARA_OPTIONS: list[dict[str, Any]] = _opts(
    ("early_riser", "I wake up early", "मैं जल्दी उठता/उठती हूँ"),
    ("late_nights", "I sleep late", "मैं देर से सोता/सोती हूँ"),
    ("regular_exercise", "I exercise regularly", "मैं नियमित व्यायाम करता/करती हूँ"),
    ("yoga_pranayama", "I do yoga or pranayama", "मैं योग या प्राणायाम करता/करती हूँ"),
    ("sedentary_work", "My work is mostly sitting", "मेरा काम अधिकतर बैठकर है"),
    ("physical_work", "My work is physically demanding", "मेरा काम शारीरिक श्रम वाला है"),
    ("daytime_sleep", "I sleep during the day", "मैं दिन में सोता/सोती हूँ"),
    ("high_stress", "My routine is stressful", "मेरी दिनचर्या तनावपूर्ण है"),
)

INTRO = {
    "title": _t("Ayurveda assessment", "आयुर्वेद मूल्यांकन"),
    "body": _t(
        "These optional questions are used in Ayurvedic practice. They describe "
        "your constitution and routine — they are not a diagnosis, and you can "
        "skip any of them.",
        "ये वैकल्पिक सवाल आयुर्वेदिक चिकित्सा में उपयोग होते हैं। ये आपकी प्रकृति और "
        "दिनचर्या बताते हैं — यह कोई निदान नहीं है, और आप कोई भी सवाल छोड़ सकते हैं।",
    ),
}

VALID_PARIKSHA = {item["key"] for item in DASHAVIDHA}
VALID_OPTIONS = {item["key"]: {o["value"] for o in item["options"]} for item in DASHAVIDHA}
VALID_ASHTASTHANA = {item["key"] for item in ASHTASTHANA}
VALID_ASHTASTHANA_OPTIONS = {
    item["key"]: {o["value"] for o in item["options"]} for item in ASHTASTHANA
}
VALID_LIFESTYLE = {item["key"] for item in LIFESTYLE_FACTORS}
VALID_LIFESTYLE_OPTIONS = {
    item["key"]: {o["value"] for o in item["options"]} for item in LIFESTYLE_FACTORS
}
VALID_AHARA = {option["value"] for option in AHARA_OPTIONS}
VALID_VIHARA = {option["value"] for option in VIHARA_OPTIONS}

# How many examination factors an Ayurvedic intake covers, versus the
# allopathic visit's core questions.
TOTAL_AYUSH_FACTORS = (
    len(DASHAVIDHA) + len(ASHTASTHANA) + len(LIFESTYLE_FACTORS) + 2  # ahara, vihara
)
