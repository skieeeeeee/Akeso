"""Patient-facing emergency wording.

Every string here is deliberately hedged: "may require", "we noticed you
described". Nothing states a condition, and nothing names a diagnosis. The
audit rule is that no sentence should be true only if a diagnosis is true.
"""

from __future__ import annotations
from app.shared.i18n import Localised, localise, t as _t




SAFETY_NOTICE = {
    "title": _t(
        "Please speak to healthcare staff now",
        "कृपया अभी स्वास्थ्य कर्मचारियों से बात करें",
    ),
    "body": _t(
        "Some of the symptoms you described may require urgent medical attention.",
        "आपने जो कुछ लक्षण बताए हैं, उनके लिए तत्काल चिकित्सा सहायता की आवश्यकता हो सकती है।",
    ),
    "disclaimer": _t(
        "This does not confirm a medical condition. It only means a health "
        "worker should look at you sooner rather than later.",
        "यह किसी बीमारी की पुष्टि नहीं करता। इसका अर्थ केवल यह है कि किसी "
        "स्वास्थ्य कर्मी को आपको जल्दी देखना चाहिए।",
    ),
    "instruction": _t(
        "Please inform nearby healthcare staff immediately. Show them this screen.",
        "कृपया तुरंत पास के स्वास्थ्य कर्मचारियों को बताएं। उन्हें यह स्क्रीन दिखाएँ।",
    ),
    "action_staff": _t("I need immediate assistance", "मुझे तुरंत सहायता चाहिए"),
    "action_continue": _t(
        "Continue answering while waiting", "इंतज़ार करते हुए जवाब देना जारी रखें"
    ),
}

# Shown persistently once a flag is active, so it cannot be dismissed away.
URGENT_BANNER = _t(
    "Marked urgent — please stay near the staff desk.",
    "अत्यावश्यक चिह्नित — कृपया स्टाफ़ डेस्क के पास रहें।",
)
