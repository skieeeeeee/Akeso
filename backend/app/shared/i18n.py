"""Localisation primitives.

One place defines what a localised value looks like and how a missing
translation resolves. Content modules build values with `t()` and readers
resolve them with `localise()` — nothing indexes `["en"]` directly, so a gap
degrades predictably instead of raising a KeyError or rendering empty.

Adding a language means: extend `Language`, add a `FALLBACK_CHAIN` entry, and
pass the new keyword to `t()` wherever the translation exists. Untranslated
strings keep working via the chain, so a language is never half-broken.
"""

from __future__ import annotations

from app.shared.enums import Language
from app.shared.translations import OVERLAYS

Localised = dict[str, str]

# English is the source language; Hindi is the most widely-understood second
# option, so it sits between a regional language and English.
_DEFAULT_TAIL: tuple[str, ...] = (Language.HINDI.value, Language.ENGLISH.value)

FALLBACK_CHAIN: dict[str, tuple[str, ...]] = {
    Language.ENGLISH.value: (Language.ENGLISH.value,),
    Language.HINDI.value: (Language.HINDI.value, Language.ENGLISH.value),
    # Marathi is written in Devanagari, and Hindi is widely read in
    # Maharashtra, Gujarat and Punjab — so Hindi is a genuine second choice
    # for these three.
    Language.MARATHI.value: (Language.MARATHI.value, *_DEFAULT_TAIL),
    Language.GUJARATI.value: (Language.GUJARATI.value, *_DEFAULT_TAIL),
    Language.PUNJABI.value: (Language.PUNJABI.value, *_DEFAULT_TAIL),
    # Tamil is the exception: Devanagari is not read in Tamil Nadu, so Hindi
    # would be no more useful than a blank. English at least shares a script
    # with the signage and the prescriptions a patient already encounters.
    Language.TAMIL.value: (Language.TAMIL.value, Language.ENGLISH.value),
}


def t(
    en: str,
    hi: str | None = None,
    *,
    mr: str | None = None,
    ta: str | None = None,
    gu: str | None = None,
    pa: str | None = None,
) -> Localised:
    """Build a localised value.

    Only supplied languages are stored, so `localise()` can tell a real
    translation from an absent one and fall back rather than showing English
    text under a Marathi key.
    """
    value: Localised = {Language.ENGLISH.value: en}
    for code, text in (
        (Language.HINDI.value, hi),
        (Language.MARATHI.value, mr),
        (Language.TAMIL.value, ta),
        (Language.GUJARATI.value, gu),
        (Language.PUNJABI.value, pa),
    ):
        if text:
            value[code] = text
    # Fill the regional languages from the overlay files, keyed by the English
    # source. An explicit keyword above always wins, so a bad overlay entry
    # can be corrected at the call site.
    for code, overlay in OVERLAYS.items():
        if code not in value:
            translated = overlay.get(en)
            if translated:
                value[code] = translated
    return value


def language_code(language: Language | str | None) -> str:
    if language is None:
        return Language.ENGLISH.value
    return language.value if isinstance(language, Language) else str(language)


def localise(value: Localised | None, language: Language | str | None) -> str:
    """Resolve a localised value, falling back down the chain.

    @returns the best available translation, or "" when the value is missing
             entirely — never a KeyError, and never a raw dict leaking into
             a response.
    """
    if not value:
        return ""
    code = language_code(language)
    for candidate in FALLBACK_CHAIN.get(code, (code, *_DEFAULT_TAIL)):
        text = value.get(candidate)
        if text:
            return text
    # Last resort: any translation at all beats an empty screen.
    return next((text for text in value.values() if text), "")


def missing_languages(value: Localised | None) -> list[str]:
    """Which supported languages this value has no translation for.

    Used by the coverage test and the translation audit, not at runtime.
    """
    if not value:
        return [language.value for language in Language]
    return [language.value for language in Language if not value.get(language.value)]


# --- Enum labels the server needs for prose ------------------------------
# The client has its own copy for badges and chips; these exist because the
# deterministic narrative is assembled server-side and has to read as one
# sentence in the patient's language.
GENDER_LABELS: dict[str, Localised] = {
    "male": t("male", "पुरुष"),
    "female": t("female", "महिला"),
    "other": t("other", "अन्य"),
    "undisclosed": t("gender not stated", "लिंग नहीं बताया"),
}

CARE_SYSTEM_LABELS: dict[str, Localised] = {
    "allopathy": t("Allopathy", "एलोपैथी"),
    "ayurveda": t("Ayurveda", "आयुर्वेद"),
    "homoeopathy": t("Homoeopathy", "होम्योपैथी"),
    "unani": t("Unani", "यूनानी"),
    "siddha": t("Siddha", "सिद्ध"),
    "yoga_naturopathy": t("Yoga and Naturopathy", "योग और प्राकृतिक चिकित्सा"),
    "unsure": t("not decided yet", "अभी तय नहीं"),
}


def enum_label(labels: dict[str, Localised], value, language) -> str:
    """A localised label for an enum value, blank when we have none."""
    key = getattr(value, "value", value)
    if not key:
        return ""
    return localise(labels.get(str(key), {}), language)
