"""Localisation plumbing.

These tests guard the property that makes adding a language safe: every
localised value resolves to *something* in every supported language, so a
missing translation degrades through the fallback chain instead of rendering
an empty screen.
"""

from __future__ import annotations

import re

import pytest

from app.shared.enums import Language
from app.shared.i18n import (
    FALLBACK_CHAIN,
    localise,
    missing_languages,
    t,
)

ALL_LANGUAGES = [language.value for language in Language]


# A string no overlay carries, so these tests exercise `t()` itself rather
# than the translation files. Overlay lookup is covered by TestOverlays.
UNTRANSLATED = "A string no translation file carries"


class TestBuilder:
    def test_english_is_always_present(self):
        assert t(UNTRANSLATED)["en"] == UNTRANSLATED

    def test_only_supplied_languages_are_stored(self):
        value = t(UNTRANSLATED, "बुखार", mr="ताप")
        # An absent translation must be absent, not silently English — that is
        # what lets `localise` fall back rather than showing the wrong language.
        assert set(value) == {"en", "hi", "mr"}

    def test_empty_strings_are_treated_as_absent(self):
        assert set(t(UNTRANSLATED, "", mr="  ".strip())) == {"en"}


class TestFallback:
    def test_exact_match_wins(self):
        assert localise(t(UNTRANSLATED, "बुखार", mr="ताप"), "mr") == "ताप"

    def test_a_devanagari_reading_language_falls_back_to_hindi(self):
        # Marathi is written in Devanagari; Gujarati and Punjabi speakers
        # widely read Hindi. For these three Hindi is a real second choice.
        for language in ("mr", "gu", "pa"):
            assert localise(t(UNTRANSLATED, "बुखार"), language) == "बुखार", language

    def test_tamil_falls_back_to_english_not_hindi(self):
        # Devanagari is not read in Tamil Nadu, so Hindi would be no more
        # useful to a Tamil patient than a blank.
        assert localise(t(UNTRANSLATED, "बुखार"), "ta") == UNTRANSLATED

    def test_hindi_falls_back_to_english(self):
        assert localise(t("Fever"), "hi") == "Fever"

    def test_english_never_falls_through_to_a_regional_language(self):
        # English must not resolve to Hindi even if only Hindi is richer.
        assert localise(t("Fever", "बुखार"), "en") == "Fever"

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_every_language_resolves_to_something(self, language: str):
        assert localise(t(UNTRANSLATED, "बुखार"), language)

    def test_a_missing_value_returns_empty_not_an_error(self):
        assert localise(None, "hi") == ""
        assert localise({}, "hi") == ""

    def test_an_unknown_language_code_still_resolves(self):
        assert localise(t(UNTRANSLATED, "बुखार"), "kn") == "बुखार"

    def test_every_supported_language_has_a_chain(self):
        assert set(FALLBACK_CHAIN) == set(ALL_LANGUAGES)

    def test_every_chain_ends_at_english(self):
        for language, chain in FALLBACK_CHAIN.items():
            assert chain[-1] == "en", language
            assert chain[0] == language


class TestCoverageAudit:
    def test_missing_languages_reports_the_gaps(self):
        assert missing_languages(t(UNTRANSLATED, "बुखार")) == ["mr", "ta", "gu", "pa"]
        assert missing_languages(None) == ALL_LANGUAGES


class TestOverlays:
    """The regional languages come from `app/shared/translations/`.

    Content modules only pass `en` and `hi`; `t()` fills the rest from the
    overlay files, keyed by the English source. These tests pin that wiring,
    not the translations themselves.
    """

    def test_the_overlay_supplies_a_regional_language(self):
        value = t("Fever", "बुखार")
        assert value["mr"] and value["ta"] and value["gu"] and value["pa"]
        assert value["mr"] != value["hi"], "Marathi must not just be Hindi"

    def test_an_inline_argument_beats_the_overlay(self):
        # This is how a wrong overlay entry gets corrected at the call site.
        assert t("Fever", "बुखार", mr="वेगळा शब्द")["mr"] == "वेगळा शब्द"

    @pytest.mark.parametrize("code", ["mr", "ta", "gu", "pa"])
    def test_no_overlay_entry_is_left_in_english(self, code: str):
        from app.shared.translations import OVERLAYS

        # An entry copied from the English source is worse than no entry: it
        # defeats the fallback chain and shows English under a regional key.
        # A fragment that is only placeholders and punctuation ("{lead}:
        # {found}.") has nothing to translate, so identity is correct there.
        import re

        def words(text: str) -> str:
            return re.sub(r"\{\w+\}|[^A-Za-z ]", "", text).strip()

        same = [
            en
            for en, text in OVERLAYS[code].items()
            if text.strip() == en.strip() and words(en)
        ]
        assert same == [], same

    @pytest.mark.parametrize("code", ["mr", "ta", "gu", "pa"])
    def test_each_translation_is_in_its_own_script(self, code: str):
        """Catches a character typed from the wrong keyboard block.

        Devanagari, Gujarati and Gurmukhi look similar enough that a single
        wrong letter is invisible on review but renders as a foreign glyph
        mid-word. This found a real one: a Devanagari ट inside a Gujarati word.
        """
        import unicodedata

        from app.shared.translations import OVERLAYS

        blocks = {
            "mr": (0x0900, 0x097F),
            "gu": (0x0A80, 0x0AFF),
            "pa": (0x0A00, 0x0A7F),
            "ta": (0x0B80, 0x0BFF),
        }
        low, high = blocks[code]
        wrong = []
        for en, text in OVERLAYS[code].items():
            for ch in text:
                point = ord(ch)
                # Latin, digits, punctuation and spacing are all legitimate.
                if point < 0x0900 or unicodedata.category(ch).startswith(("P", "Z", "C")):
                    continue
                if not low <= point <= high:
                    wrong.append((en, ch, f"U+{point:04X}"))
        assert wrong == [], wrong

    @pytest.mark.parametrize("code", ["mr", "ta", "gu", "pa"])
    def test_placeholders_survive_translation(self, code: str):
        from app.shared.translations import OVERLAYS

        # A narrative fragment that loses its {placeholder} renders the
        # literal token to the patient, or drops their answer entirely.
        import re

        for en, text in OVERLAYS[code].items():
            expected = set(re.findall(r"\{(\w+)\}", en))
            actual = set(re.findall(r"\{(\w+)\}", text))
            assert expected == actual, (code, en)


class TestContentResolvesEverywhere:
    """Every string a patient can see must resolve in every language."""

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_assessment_questions(self, language: str):
        from app.modules.accessibility.content import ASSESSMENT_QUESTIONS

        for question in ASSESSMENT_QUESTIONS:
            assert localise(question["prompt"], language), question["id"]
            assert localise(question["help"], language), question["id"]
            for option in question["options"]:
                assert localise(option["label"], language), option["value"]

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_interview_questions(self, language: str):
        from app.modules.interview.questions import QUESTIONS, SECTIONS

        for section in SECTIONS:
            assert localise(section.title, language), section.key
            assert localise(section.intro, language), section.key
        for question in QUESTIONS:
            assert localise(question.prompt, language), question.id
            assert localise(question.help, language), question.id
            for option in question.options:
                assert localise(option.label, language), option.value

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_encounter_script(self, language: str):
        from app.modules.encounter.script import QUESTIONS, SECTIONS

        for section in SECTIONS:
            assert localise(section.title, language), section.key
        for question in QUESTIONS:
            assert localise(question.prompt, language), question.id
            assert localise(question.help, language), question.id

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_consent_text(self, language: str):
        from app.modules.consent.content import CONSENT_ITEMS, CONSENT_SUMMARY

        for key in ("title", "body", "withdraw"):
            assert localise(CONSENT_SUMMARY[key], language), key
        for item in CONSENT_ITEMS:
            for key in ("title", "what", "why", "how"):
                assert localise(item[key], language), (item["purpose"], key)

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_emergency_wording(self, language: str):
        from app.modules.red_flags.content import SAFETY_NOTICE

        for key, value in SAFETY_NOTICE.items():
            assert localise(value, language), key

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_ayush_content(self, language: str):
        from app.modules.ayush.content import (
            AHARA_OPTIONS,
            DASHAVIDHA,
            VIHARA_OPTIONS,
        )

        for factor in DASHAVIDHA:
            assert localise(factor["prompt"], language), factor["key"]
            for option in factor["options"]:
                assert localise(option["label"], language), option["value"]
        for option in [*AHARA_OPTIONS, *VIHARA_OPTIONS]:
            assert localise(option["label"], language), option["value"]

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_medical_sections(self, language: str):
        from app.modules.medical_history.content import MEDICAL_SECTIONS

        for section in MEDICAL_SECTIONS:
            assert localise(section["title"], language), section["key"]
            assert localise(section["prompt"], language), section["key"]


class TestPatientFacingProseIsLocalised:
    """The narratives are the patient's last look before a doctor sees it.

    They are assembled server-side, so a missing fragment shows up as an
    English sentence in the middle of a Hindi page rather than as a blank.
    """

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_section_labels_resolve(self, language: str):
        from app.modules.medical_history.structured import (
            SECTION_LABELS_LOCALISED,
            section_labels,
        )

        labels = section_labels(language)
        assert set(labels) == set(SECTION_LABELS_LOCALISED)
        assert all(labels.values())

    @pytest.mark.parametrize("language", ALL_LANGUAGES)
    def test_narrative_fragments_resolve(self, language: str):
        from app.modules.encounter.summary import DISCLAIMER, _COPY
        from app.modules.medical_history.structured import (
            _NARRATIVE_COPY,
            _NARRATIVE_LEADS,
            NONE_REPORTED_LABEL,
        )

        for key, value in {**_COPY, **_NARRATIVE_COPY}.items():
            assert localise(value, language), key
        for key, lead in _NARRATIVE_LEADS:
            assert localise(lead, language), key
        assert localise(DISCLAIMER, language)
        assert localise(NONE_REPORTED_LABEL, language)

    def test_a_hindi_patient_gets_a_hindi_visit_narrative(self):
        """No Latin script in the fragments the template contributes."""
        from types import SimpleNamespace

        from app.modules.encounter.summary import template_narrative
        from app.shared.enums import Gender, RedFlagStatus, VisitType

        patient = SimpleNamespace(age=71, gender=Gender.FEMALE, full_name="कमला देवी")
        encounter = SimpleNamespace(
            chief_complaint="घुटनों में दर्द",
            visit_type=VisitType.FOLLOW_UP,
            structured_history={
                "history_of_present_illness": [{"value": "सुबह ज़्यादा"}, {"value": "7/10"}],
            },
            red_flag_status=RedFlagStatus.ACTIVE,
        )
        existing = SimpleNamespace(conditions=["गठिया"], medications=[], allergies=[])

        text = template_narrative(patient, encounter, existing, "hi")
        # The severity metric is the only Latin-script content we expect.
        assert "7/10" in text
        assert not re.search(r"[A-Za-z]", text.replace("7/10", ""))
        # Safety wording survives localisation.
        assert "निदान नहीं" in text
        assert "तत्काल" in text

    def test_the_english_narrative_is_unchanged_by_localisation(self):
        from types import SimpleNamespace

        from app.modules.encounter.summary import template_narrative
        from app.shared.enums import Gender, RedFlagStatus, VisitType

        patient = SimpleNamespace(age=52, gender=Gender.MALE, full_name="Rajesh Kumar")
        encounter = SimpleNamespace(
            chief_complaint="Cough",
            visit_type=VisitType.FIRST_VISIT,
            structured_history={},
            red_flag_status=RedFlagStatus.NONE,
        )
        existing = SimpleNamespace(conditions=[], medications=[], allergies=[])

        text = template_narrative(patient, encounter, existing, "en")
        assert text.startswith("Rajesh Kumar (52-year-old, male) presents reporting: Cough.")
        assert "This is not a diagnosis." in text
