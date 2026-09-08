"""Red-flag detection criteria.

DELIBERATELY NOT EXPOSED THROUGH THE API.

This module is the only place the triggering criteria live. Nothing here is
serialised into an API response, an error message, or the OpenAPI schema —
`app/modules/red_flags/schemas.py` returns a category and a patient-facing
message, never the phrase that matched.

Two reasons:

1. Safety. A patient who can read the trigger list can also construct answers
   that dodge it, or fake an emergency to skip the interview.
2. Honesty. These are screening heuristics for prioritising a queue, not
   diagnostic criteria, and publishing them would invite them to be read as
   the latter.

Detection is rule-first. An AI assist may *raise* a concern the rules missed,
but it is bounded to the same category set and can never clear a flag.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.shared.enums import RedFlagCategory

# Severity threshold on the 1-10 scale above which pain is escalated when it
# occurs alongside a concerning site.
_SEVERE_SCORE = 8


@dataclass(frozen=True, slots=True)
class _Criterion:
    category: RedFlagCategory
    # Compiled privately; never rendered.
    pattern: re.Pattern[str]
    # Requires a second corroborating signal before firing, to reduce false
    # positives on phrases like "no chest pain".
    needs_support: bool = False


def _p(*alternatives: str) -> re.Pattern[str]:
    return re.compile(r"(?:" + "|".join(alternatives) + r")", re.IGNORECASE)


# Negations are checked first: "no bleeding" must not fire the bleeding rule.
_NEGATION = re.compile(
    r"\b(?:no|not|never|without|denies|nahi|nahin|kuch nahi)\b[^.;]{0,24}$",
    re.IGNORECASE,
)

# Hindi negates after the phrase, not before it: "सीने में दर्द नहीं है" is a
# denial, but every word before the negator reads as an affirmation. So the
# text *following* a Devanagari hit is checked too. Patterns that themselves
# end in a negator ("साँस नहीं आ") are unaffected: they consume it, so what
# follows them is not another negator.
_NEGATION_AFTER = re.compile(r"^[^।.;]{0,18}(?:नहीं|नही|बिल्कुल नहीं)")

_CRITERIA: tuple[_Criterion, ...] = (
    _Criterion(
        RedFlagCategory.BREATHING,
        _p(
            r"can(?:'|no)?t breathe", r"cannot breathe", r"unable to breathe",
            r"gasping", r"choking", r"struggling to breathe",
            r"severe(?:ly)? breathless", r"saans nahi", r"dam ghut",
            r"blue lips", r"lips turn(?:ing)? blue",
            # Devanagari: the interface is fully Hindi, so a Hindi patient
            # types and dictates in Hindi script, not in transliteration.
            r"साँ?स नहीं", r"सांस नहीं", r"दम घुट", r"होंठ नीले",
            r"साँ?स लेने में बहुत", r"सांस लेने में बहुत",
        ),
    ),
    _Criterion(
        RedFlagCategory.CHEST,
        _p(
            r"crushing chest", r"chest.{0,12}(?:crush|tight|pressure|heavi)",
            r"pain.{0,20}(?:left arm|jaw|radiat)", r"seene me bhari",
            r"chhaati.{0,12}dabav", r"cold sweat.{0,20}chest",
            r"(?:सीने|छाती).{0,14}(?:भारी|दबाव|जकड़न|दबा)",
            r"(?:बाएँ|बाएं|बायें).{0,10}(?:हाथ|बाँह|बांह).{0,12}दर्द",
            r"जबड़े.{0,12}दर्द", r"ठंडा पसीना",
        ),
    ),
    _Criterion(
        RedFlagCategory.BLEEDING,
        _p(
            r"bleeding.{0,16}(?:heavil|won'?t stop|not stopping|profus)",
            r"vomiting blood", r"coughing (?:up )?blood", r"blood in vomit",
            r"khoon.{0,12}(?:band nahi|bahut)", r"soaking through",
            r"(?:खून|ख़ून).{0,14}(?:बंद नहीं|बहुत|रुक नहीं)",
            r"(?:उल्टी|खाँसी|खांसी).{0,12}(?:में )?(?:खून|ख़ून)",
            r"(?:खून|ख़ून) की उल्टी",
        ),
    ),
    _Criterion(
        RedFlagCategory.CONSCIOUSNESS,
        _p(
            r"(?:passed|blacked) out", r"lost consciousness", r"unconscious",
            r"fainted", r"behosh", r"unresponsive", r"had a (?:fit|seizure)",
            r"convuls",
            r"बेहोश", r"बेहोशी", r"होश नहीं", r"दौरा पड़", r"मिर्गी",
        ),
    ),
    _Criterion(
        RedFlagCategory.NEUROLOGICAL,
        _p(
            r"sudden.{0,20}(?:weakness|numbness|paralysis)",
            r"can(?:'|no)?t (?:move|speak|feel).{0,16}(?:arm|leg|side|face)",
            r"face.{0,12}droop", r"slurred speech", r"worst headache",
            r"sudden.{0,16}(?:blind|vision loss)", r"lakwa", r"bol nahi",
            r"लकवा", r"लक़वा", r"बोल नहीं",
            r"अचानक.{0,16}(?:कमज़ोरी|कमजोरी|सुन्न|लकवा)",
            r"(?:हाथ|पैर|मुँह|मुंह).{0,14}(?:नहीं उठ|सुन्न|टेढ़ा)",
            r"अचानक.{0,16}(?:दिखाई नहीं|अंधा)",
            r"बहुत तेज़? सिरदर्द",
        ),
    ),
)

# Sites where a severe pain score is itself concerning.
_SEVERE_PAIN_SITES = _p(
    r"chest", r"seene", r"chhaati", r"head", r"sir", r"abdomen", r"pet",
    r"सीने", r"छाती", r"सिर", r"पेट",
)


@dataclass(frozen=True, slots=True)
class RuleHit:
    """A criterion that matched. `evidence` is the patient's own words."""

    category: RedFlagCategory
    # Quoted from the patient so a clinician can see why it fired. This is
    # safe to store and show; the *pattern* is not.
    evidence: str


def _mentions(text: str, criterion: _Criterion) -> bool:
    match = criterion.pattern.search(text)
    if match is None:
        return False
    # Reject a negated mention: English negates before the phrase...
    preceding = text[max(0, match.start() - 28) : match.start()]
    if _NEGATION.search(preceding) is not None:
        return False
    # ...and Hindi negates after it.
    return _NEGATION_AFTER.search(text[match.end() :]) is None


def evaluate(texts: list[str], severity_score: int | None = None) -> list[RuleHit]:
    """Screen a patient's own words for urgent presentations.

    @param texts free-text answers from the current encounter only.
    @param severity_score the 1-10 rating, when the patient gave one.
    @returns one hit per category, at most — categories do not stack.
    """
    hits: dict[RedFlagCategory, RuleHit] = {}

    for raw in texts:
        text = re.sub(r"\s+", " ", raw or "").strip()
        if not text:
            continue
        for criterion in _CRITERIA:
            if criterion.category in hits:
                continue
            if _mentions(text, criterion):
                hits[criterion.category] = RuleHit(
                    category=criterion.category, evidence=text[:240]
                )

    # A very high self-rated severity at a concerning site is escalated even
    # when no specific phrase matched.
    if severity_score is not None and severity_score >= _SEVERE_SCORE:
        for raw in texts:
            if _SEVERE_PAIN_SITES.search(raw or ""):
                hits.setdefault(
                    RedFlagCategory.OTHER,
                    RuleHit(
                        category=RedFlagCategory.OTHER,
                        evidence=re.sub(r"\s+", " ", raw).strip()[:240],
                    ),
                )
                break

    return list(hits.values())


def parse_severity(value: str | None) -> int | None:
    """Read a stored severity answer such as "8/10"."""
    if not value:
        return None
    match = re.search(r"\d+", value)
    if not match:
        return None
    score = int(match.group())
    return score if 1 <= score <= 10 else None
