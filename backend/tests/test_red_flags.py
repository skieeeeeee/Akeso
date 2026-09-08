"""Red-flag screening.

The rules module is pure, so it is tested directly. These tests defend the
safety behaviour AND the property that the criteria are not discoverable
through the API.
"""

from __future__ import annotations

import pytest

from app.modules.red_flags import rules
from app.modules.red_flags.content import SAFETY_NOTICE
from app.shared.enums import RedFlagCategory


class TestDetection:
    @pytest.mark.parametrize(
        "text,category",
        [
            ("I can't breathe properly", RedFlagCategory.BREATHING),
            ("gasping for air since morning", RedFlagCategory.BREATHING),
            ("crushing chest pain spreading to my left arm", RedFlagCategory.CHEST),
            ("seene me bhari dabav hai", RedFlagCategory.CHEST),
            ("vomiting blood since morning", RedFlagCategory.BLEEDING),
            ("the bleeding won't stop", RedFlagCategory.BLEEDING),
            ("he passed out for a minute", RedFlagCategory.CONSCIOUSNESS),
            ("behosh ho gaya tha", RedFlagCategory.CONSCIOUSNESS),
            ("sudden weakness on my right side", RedFlagCategory.NEUROLOGICAL),
            ("my speech is slurred and my face is drooping", RedFlagCategory.NEUROLOGICAL),
        ],
    )
    def test_urgent_presentations_are_caught(self, text: str, category):
        hits = rules.evaluate([text])
        assert category in {hit.category for hit in hits}

    @pytest.mark.parametrize(
        "text",
        [
            "mild fever and a headache",
            "stomach pain since yesterday",
            "I need a repeat prescription",
            "knee pain when climbing stairs",
            "cough for three days",
        ],
    )
    def test_ordinary_complaints_are_not_flagged(self, text: str):
        assert rules.evaluate([text]) == []

    @pytest.mark.parametrize(
        "text",
        [
            "no chest pain, just a mild cough",
            "not bleeding at all",
            "never passed out",
            "denies any breathlessness",
        ],
    )
    def test_a_negated_mention_does_not_fire(self, text: str):
        assert rules.evaluate([text]) == []

    def test_severe_pain_at_a_concerning_site_escalates(self):
        assert rules.evaluate(["chest pain"], 9) != []
        # ...but a mild score at the same site does not.
        assert rules.evaluate(["chest pain"], 3) == []

    def test_severe_pain_elsewhere_does_not_escalate(self):
        assert rules.evaluate(["ankle pain"], 10) == []

    def test_a_category_does_not_stack(self):
        hits = rules.evaluate(["can't breathe", "still cannot breathe", "gasping"])
        assert len([h for h in hits if h.category == RedFlagCategory.BREATHING]) == 1

    def test_evidence_quotes_the_patient(self):
        hits = rules.evaluate(["I have been vomiting blood since morning"])
        assert "vomiting blood" in hits[0].evidence

    def test_empty_input_is_safe(self):
        assert rules.evaluate([]) == []
        assert rules.evaluate(["", "   "]) == []

    @pytest.mark.parametrize("raw,expected", [("8/10", 8), ("10", 10), (None, None), ("abc", None), ("99", None)])
    def test_severity_parsing(self, raw, expected):
        assert rules.parse_severity(raw) == expected


class TestSafetyLanguage:
    """The wording must never assert a condition."""

    def test_every_string_is_translated(self):
        for key, value in SAFETY_NOTICE.items():
            assert set(value) == {"en", "hi", "mr", "ta", "gu", "pa"}, key
            assert value["en"] and value["hi"], key

    def test_it_says_may_require_not_you_have(self):
        assert "may require" in SAFETY_NOTICE["body"]["en"]
        assert "does not confirm" in SAFETY_NOTICE["disclaimer"]["en"]

    @pytest.mark.parametrize(
        "forbidden",
        ["heart attack", "stroke", "you have", "diagnosed", "emergency room", "you are having"],
    )
    def test_it_names_no_condition(self, forbidden: str):
        combined = " ".join(v["en"].lower() for v in SAFETY_NOTICE.values())
        assert forbidden not in combined

    def test_it_directs_the_patient_to_staff(self):
        assert "staff" in SAFETY_NOTICE["instruction"]["en"].lower()


class TestCriteriaArePrivate:
    """The trigger phrases must not be reachable through the API surface."""

    def test_the_schemas_do_not_carry_criteria(self):
        from app.modules.red_flags.schemas import RedFlagOut, RedFlagStateOut

        for model in (RedFlagOut, RedFlagStateOut):
            fields = set(model.model_fields)
            assert not fields & {"pattern", "criteria", "patterns", "keywords", "rules"}

    def test_the_openapi_schema_leaks_no_trigger_phrases(self):
        from app.main import app

        schema = str(app.openapi()).lower()
        # A sample of distinctive trigger phrases from the private rules.
        for phrase in ("crushing chest", "vomiting blood", "slurred speech", "behosh", "gasping"):
            assert phrase not in schema, f"{phrase!r} leaked into the public schema"

    def test_there_is_no_endpoint_to_clear_a_flag(self):
        from app.main import app

        paths = [route.path for route in app.routes if hasattr(route, "methods")]
        for path in paths:
            assert "clear" not in path.lower()
            assert "priority" not in path.lower()


class TestHindiScriptIsScreened:
    """The interface is fully Hindi, so a Hindi patient answers in Hindi
    script. Screening that only understood transliteration would silently
    stop working for exactly the patients most likely to need it.

    Trigger phrases stay private — these tests live beside the rules module
    and are never served, the same as the criteria themselves.
    """

    @pytest.mark.parametrize(
        "text,category",
        [
            ("साँस नहीं आ रही है", RedFlagCategory.BREATHING),
            ("दम घुट रहा है", RedFlagCategory.BREATHING),
            ("सीने में भारीपन है", RedFlagCategory.CHEST),
            ("छाती में दबाव और बाएँ हाथ में दर्द", RedFlagCategory.CHEST),
            ("उल्टी में खून आया", RedFlagCategory.BLEEDING),
            ("खून बंद नहीं हो रहा", RedFlagCategory.BLEEDING),
            ("कल बेहोश हो गए थे", RedFlagCategory.CONSCIOUSNESS),
            ("अचानक कमजोरी और मुँह टेढ़ा हो गया", RedFlagCategory.NEUROLOGICAL),
            ("बोल नहीं पा रहे", RedFlagCategory.NEUROLOGICAL),
        ],
    )
    def test_it_fires_on_hindi_script(self, text: str, category):
        hits = rules.evaluate([text])
        assert [hit.category for hit in hits] == [category], text

    @pytest.mark.parametrize(
        "text",
        [
            # Each of these matches a criterion and is then denied, so it
            # only passes because the trailing negator is read.
            "सीने में भारीपन नहीं है",
            "बेहोश नहीं हुए",
            "खून की उल्टी नहीं हुई",
            "लकवा नहीं है",
        ],
    )
    def test_a_hindi_denial_does_not_fire(self, text: str):
        # Hindi puts the negator after the phrase, so a denial reads as an
        # affirmation to a rule that only looks backwards.
        assert rules.evaluate([text]) == []

    def test_a_severe_score_at_a_hindi_named_site_escalates(self):
        hits = rules.evaluate(["सीने में दर्द"], severity_score=9)
        assert [hit.category for hit in hits] == [RedFlagCategory.OTHER]

    def test_the_hindi_criteria_are_not_served(self, client, api):
        """Same constraint as the English phrases: never in the schema."""
        schema = client.get("/openapi.json").text
        for phrase in ("बेहोश", "लकवा", "दम घुट", "सीने में भारी"):
            assert phrase not in schema, phrase
