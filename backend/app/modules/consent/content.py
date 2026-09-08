"""Consent text.

Versioned (`CONSENT_TEXT_VERSION`) and stored with each record, so we always
know which wording a patient actually agreed to.
"""

from __future__ import annotations

from typing import Any

from app.shared.enums import ConsentPurpose
from app.shared.i18n import Localised, localise, t as _t

CONSENT_TEXT_VERSION = "2026-01"




CONSENT_ITEMS: list[dict[str, Any]] = [
    {
        "purpose": ConsentPurpose.HEALTH_DATA_COLLECTION.value,
        "required": True,
        "title": _t("Collecting your health information", "आपकी स्वास्थ्य जानकारी एकत्र करना"),
        "what": _t(
            "Your symptoms, past illnesses, surgeries, medicines, allergies and family history.",
            "आपके लक्षण, पिछली बीमारियाँ, ऑपरेशन, दवाइयाँ, एलर्जी और पारिवारिक इतिहास।",
        ),
        "why": _t(
            "So your doctor already knows your history and can spend the visit on your actual problem.",
            "जिससे आपके डॉक्टर को आपका इतिहास पहले से पता हो और वे मुलाक़ात में आपकी असल समस्या पर ध्यान दे सकें।",
        ),
        "how": _t(
            "It is stored against your patient record and shown to the clinician treating you.",
            "यह आपके रोगी रिकॉर्ड में सुरक्षित रखी जाती है और आपका इलाज करने वाले चिकित्सक को दिखाई जाती है।",
        ),
    },
    {
        "purpose": ConsentPurpose.SHARE_WITH_TREATING_DOCTOR.value,
        "required": True,
        "title": _t("Sharing with your doctor", "आपके डॉक्टर के साथ साझा करना"),
        "what": _t(
            "A summary of what you tell us today, and any records you upload.",
            "आज आप जो बताते हैं उसका सारांश, और आपके अपलोड किए गए रिकॉर्ड।",
        ),
        "why": _t(
            "Your doctor needs this to understand your case before you walk in.",
            "आपके डॉक्टर को आपकी स्थिति समझने के लिए यह ज़रूरी है।",
        ),
        "how": _t(
            "Only clinicians involved in your care can see it.",
            "केवल आपकी देखभाल में शामिल चिकित्सक ही इसे देख सकते हैं।",
        ),
    },
    {
        "purpose": ConsentPurpose.ABHA_LINKAGE.value,
        "required": False,
        "title": _t("Linking your health ID", "आपकी हेल्थ आईडी जोड़ना"),
        "what": _t(
            "The health ID number you entered, linked to this patient record.",
            "आपके द्वारा दर्ज हेल्थ आईडी नंबर, इस रोगी रिकॉर्ड से जुड़ा हुआ।",
        ),
        "why": _t(
            "So your records can follow you between visits instead of starting over.",
            "जिससे आपके रिकॉर्ड हर मुलाक़ात में नए सिरे से शुरू होने के बजाय आपके साथ चलें।",
        ),
        "how": _t(
            "This is a prototype and is not connected to the national ABDM network.",
            "यह एक प्रोटोटाइप है और राष्ट्रीय ABDM नेटवर्क से जुड़ा नहीं है।",
        ),
    },
]

# Shown above the list, in plain language.
CONSENT_SUMMARY = {
    "title": _t("Before we begin", "शुरू करने से पहले"),
    "body": _t(
        "We will ask about your health so your doctor is prepared before you meet. "
        "You choose what to share, and you can withdraw your consent at any time.",
        "हम आपके स्वास्थ्य के बारे में पूछेंगे जिससे आपके डॉक्टर आपसे मिलने से पहले तैयार हों। "
        "आप तय करते हैं कि क्या साझा करना है, और आप अपनी सहमति कभी भी वापस ले सकते हैं।",
    ),
    "withdraw": _t(
        "You can withdraw consent later from your profile. Nothing is shared without your agreement.",
        "आप बाद में अपनी प्रोफ़ाइल से सहमति वापस ले सकते हैं। आपकी सहमति के बिना कुछ भी साझा नहीं किया जाता।",
    ),
}

REQUIRED_PURPOSES: tuple[ConsentPurpose, ...] = tuple(
    ConsentPurpose(item["purpose"]) for item in CONSENT_ITEMS if item["required"]
)
