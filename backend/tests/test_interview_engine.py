"""The conversation state engine.

Pure, so it is tested directly. These tests encode the rules that keep the
workflow under application control rather than the model's.
"""

from __future__ import annotations

import pytest

from app.modules.interview import engine
from app.modules.interview.questions import question_by_id


def walk(state: engine.InterviewState, answers: dict[str, str], limit: int = 60):
    """Answer questions until the interview ends, recording what was asked."""
    asked: list[tuple[str, str]] = []
    for _ in range(limit):
        scheduled = engine.next_question(state)
        if scheduled is None:
            return asked
        state.current_section = scheduled.question.section
        asked.append((scheduled.question.id, scheduled.item))
        engine.apply_answer(state, scheduled, answers.get(scheduled.question.id, "no"))
    raise AssertionError("interview did not terminate")


class TestNormalisation:
    @pytest.mark.parametrize(
        "raw,expected",
        [("  chest   pain ", "chest pain"), ("Fever.", "Fever"), ("", "")],
    )
    def test_whitespace_and_punctuation(self, raw: str, expected: str):
        assert engine.normalize(raw) == expected

    @pytest.mark.parametrize("raw", ["no", "None", "nahi", "kuch nahi", "not sure", "NIL"])
    def test_negatives_in_both_languages(self, raw: str):
        assert engine.is_negative(raw)

    @pytest.mark.parametrize("raw", ["yes", "haan", "ji haan", "yep"])
    def test_affirmatives(self, raw: str):
        assert engine.is_affirmative(raw)

    def test_splits_a_spoken_list(self):
        # STT rarely produces clean punctuation.
        assert engine.split_list("diabetes and high blood pressure") == [
            "diabetes",
            "high blood pressure",
        ]
        assert engine.split_list("metformin, aspirin aur telmisartan") == [
            "metformin",
            "aspirin",
            "telmisartan",
        ]


class TestScheduling:
    def test_starts_with_the_chief_complaint(self):
        assert engine.next_question(engine.InterviewState()).question.id == "q_chief_complaint"

    def test_a_no_gate_skips_its_list_question(self):
        state = engine.InterviewState()
        asked = [qid for qid, _ in walk(state, {"q_chief_complaint": "Fever"})]
        # Said "no" to every gate, so no gated list question was asked.
        assert "q_has_conditions" in asked
        assert "q_conditions" not in asked
        assert "q_surgeries" not in asked
        assert "q_investigations" not in asked

    def test_a_yes_gate_opens_its_list_question(self):
        state = engine.InterviewState()
        asked = [
            qid
            for qid, _ in walk(
                state,
                {
                    "q_chief_complaint": "Fever",
                    "q_has_conditions": "yes",
                    "q_conditions": "Diabetes",
                    "q_condition_medicine": "no",
                },
            )
        ]
        assert "q_conditions" in asked

    def test_ayush_is_only_walked_when_opted_in(self):
        without = engine.InterviewState()
        assert "ayush" not in engine.active_sections(without)

        with_ayush = engine.InterviewState(enabled_sections=["ayush"])
        assert "ayush" in engine.active_sections(with_ayush)

    def test_the_interview_terminates(self):
        state = engine.InterviewState()
        asked = walk(state, {"q_chief_complaint": "Fever"})
        assert engine.next_question(state) is None
        assert len(asked) >= 8


class TestBranching:
    """The spec's worked example, end to end."""

    def test_condition_leads_to_medicine_then_its_name(self):
        state = engine.InterviewState()
        conditions = question_by_id("q_conditions")

        engine.apply_answer(state, engine.Scheduled(question_by_id("q_has_conditions"), instance_id="q_has_conditions"), "yes")
        applied = engine.apply_answer(
            state, engine.Scheduled(conditions, instance_id="q_conditions"), "diabetes"
        )
        assert applied.items == ["Diabetes"]
        assert len(applied.queued) == 2

        first = engine.next_question(state)
        assert first.question.id == "q_condition_medicine"
        assert first.item == "Diabetes"
        # The prompt is rendered with the item substituted in.
        assert "Diabetes" in first.prompt("en", False)
        engine.apply_answer(state, first, "yes")

        second = engine.next_question(state)
        assert second.question.id == "q_condition_medicine_name"
        assert "Diabetes" in second.prompt("en", False)
        engine.apply_answer(state, second, "Metformin 500 mg")
        assert state.answers[engine.instance_key("q_condition_medicine_name", "Diabetes")] == "Metformin 500 mg"

    def test_saying_no_to_medicine_skips_asking_its_name(self):
        state = engine.InterviewState()
        engine.apply_answer(state, engine.Scheduled(question_by_id("q_has_conditions"), instance_id="q_has_conditions"), "yes")
        engine.apply_answer(
            state,
            engine.Scheduled(question_by_id("q_conditions"), instance_id="q_conditions"),
            "asthma",
        )
        medicine = engine.next_question(state)
        engine.apply_answer(state, medicine, "no")

        following = engine.next_question(state)
        assert not (
            following
            and following.question.id == "q_condition_medicine_name"
            and following.item == "Asthma"
        )

    def test_each_condition_gets_its_own_branch(self):
        state = engine.InterviewState()
        engine.apply_answer(state, engine.Scheduled(question_by_id("q_has_conditions"), instance_id="q_has_conditions"), "yes")
        engine.apply_answer(
            state,
            engine.Scheduled(question_by_id("q_conditions"), instance_id="q_conditions"),
            "diabetes and asthma",
        )
        items = set()
        for _ in range(4):
            scheduled = engine.next_question(state)
            if scheduled is None or scheduled.question.id.startswith("q_has"):
                break
            items.add(scheduled.item)
            engine.apply_answer(state, scheduled, "no")
        assert {"Diabetes", "Asthma"} <= items

    def test_a_question_is_never_asked_twice(self):
        state = engine.InterviewState()
        asked = walk(state, {"q_chief_complaint": "Fever", "q_has_conditions": "yes",
                             "q_conditions": "Diabetes", "q_condition_medicine": "no"})
        assert len(asked) == len(set(asked))


class TestAnswerHandling:
    def test_an_empty_answer_re_asks_then_moves_on(self):
        state = engine.InterviewState()
        scheduled = engine.next_question(state)

        first = engine.apply_answer(state, scheduled, "")
        assert first.retry is True
        assert engine.next_question(state).question.id == scheduled.question.id

        second = engine.apply_answer(state, scheduled, "")
        # Bounded: the patient is not trapped on one question.
        assert second.retry is False
        assert engine.next_question(state).question.id != scheduled.question.id

    def test_a_none_answer_is_recorded_rather_than_left_blank(self):
        state = engine.InterviewState()
        applied = engine.apply_answer(
            state, engine.Scheduled(question_by_id("q_allergies"), instance_id="q_allergies"), "nahi"
        )
        assert applied.items == [engine.NONE_REPORTED]

    def test_a_scale_answer_is_normalised(self):
        state = engine.InterviewState()
        applied = engine.apply_answer(
            state, engine.Scheduled(question_by_id("q_severity"), instance_id="q_severity"), "8"
        )
        assert applied.items == ["8/10"]

    def test_duplicates_within_one_answer_collapse(self):
        state = engine.InterviewState()
        applied = engine.apply_answer(
            state,
            engine.Scheduled(question_by_id("q_medications"), instance_id="q_medications"),
            "metformin, Metformin and aspirin",
        )
        assert applied.items == ["Metformin", "Aspirin"]

    def test_going_back_reopens_the_last_question(self):
        state = engine.InterviewState()
        first = engine.next_question(state)
        engine.apply_answer(state, first, "Chest pain")
        assert engine.next_question(state).question.id != first.question.id

        engine.go_back(state)
        assert engine.next_question(state).question.id == first.question.id
        # And the old answer is cleared so it can be replaced.
        assert first.key not in state.answers


class TestAiSuggestionsAreBounded:
    """The engine, not the model, decides whether a suggestion is asked."""

    def test_a_suggestion_is_asked_with_its_own_text(self):
        state = engine.InterviewState()
        assert engine.enqueue_suggested(
            state,
            prompt={"en": "How long has the cough lasted?", "hi": "खांसी कब से है?"},
            target="history_of_present_illness",
            tag="cough",
        )
        scheduled = engine.next_question(state)
        assert scheduled.prompt("en", False) == "How long has the cough lasted?"
        assert scheduled.prompt("hi", False) == "खांसी कब से है?"
        assert scheduled.target == "history_of_present_illness"

    def test_duplicate_suggestions_are_refused(self):
        state = engine.InterviewState()
        engine.enqueue_suggested(state, prompt={"en": "a", "hi": "b"}, target="allergies", tag="x")
        assert not engine.enqueue_suggested(
            state, prompt={"en": "a", "hi": "b"}, target="allergies", tag="x"
        )

    def test_a_model_cannot_flood_the_interview(self):
        state = engine.InterviewState()
        accepted = [
            engine.enqueue_suggested(
                state, prompt={"en": f"q{i}", "hi": f"q{i}"}, target="allergies", tag=f"t{i}"
            )
            for i in range(6)
        ]
        assert sum(accepted) == 2


class TestProgress:
    def test_progress_advances_and_never_exceeds_total(self):
        state = engine.InterviewState()
        seen = []
        for _ in range(40):
            scheduled = engine.next_question(state)
            if scheduled is None:
                break
            state.current_section = scheduled.question.section
            engine.apply_answer(state, scheduled, "no")
            progress = engine.progress(state)
            seen.append(progress.percent)
            assert progress.answered <= progress.total
            assert 0 <= progress.percent <= 100
        assert seen == sorted(seen)
        assert seen[-1] > seen[0]
