"""The conversation state engine.

Pure functions over an immutable-ish state object: no I/O, no AI, no database.
This is what "the AI does not control the workflow" means concretely — the
engine alone decides what is asked next, and it is fully testable without a
model or a network.

Answer normalisation happens here too, so voice, typing and touch all collapse
to the same shape before anything clinical sees them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from typing import Protocol

from app.modules.interview.questions import (
    SECTION_ORDER,
    Question,
    Section,
    base_questions_for,
    question_by_id,
)


class Script(Protocol):
    """A set of sections and questions the engine can walk.

    Phase 2's medical-history script and Phase 3's encounter script are two
    implementations, so the state machine, branching, normalisation and
    progress logic are shared rather than duplicated.
    """

    section_order: list[str]

    def sections_by_key(self) -> dict[str, Section]: ...
    def base_questions_for(self, section: str) -> list[Question]: ...
    def question_by_id(self, question_id: str) -> Question | None: ...


class ProfileScript:
    """The first-time medical-history script (Phase 2)."""

    name = "profile"

    @property
    def section_order(self) -> list[str]:
        return list(SECTION_ORDER)

    def sections_by_key(self) -> dict[str, Section]:
        from app.modules.interview.questions import SECTION_BY_KEY

        return SECTION_BY_KEY

    def base_questions_for(self, section: str) -> list[Question]:
        return base_questions_for(section)

    def question_by_id(self, question_id: str) -> Question | None:
        return question_by_id(question_id)


PROFILE_SCRIPT = ProfileScript()
from app.shared.enums import AnswerKind, Language
from app.shared.i18n import localise

NONE_REPORTED = "None reported"

_NEGATIVE = {
    "no", "none", "nope", "nothing", "nil", "na", "n/a", "no thanks",
    "nahi", "nahin", "kuch nahi", "koi nahi", "skip", "dont know",
    "don't know", "not sure", "no idea", "never",
}
_AFFIRMATIVE = {"yes", "yeah", "yep", "haan", "haa", "ha", "ji", "ji haan", "correct"}


def normalize(text: str) -> str:
    """Collapse whitespace and strip trailing punctuation from any answer."""
    cleaned = re.sub(r"\s+", " ", text or "").strip()
    return cleaned.rstrip(" .!,;")


def is_negative(text: str) -> bool:
    return normalize(text).lower() in _NEGATIVE


def is_affirmative(text: str) -> bool:
    return normalize(text).lower() in _AFFIRMATIVE


def split_list(text: str) -> list[str]:
    """Split a spoken or typed list. STT rarely produces clean commas."""
    parts = re.split(r"\s*(?:,|;|/|\band\b|\+|\n|\baur\b)\s*", normalize(text), flags=re.I)
    return [re.sub(r"^[-•*\s]+", "", part).strip() for part in parts if part.strip()]


def sentence_case(text: str) -> str:
    cleaned = normalize(text)
    return cleaned[0].upper() + cleaned[1:] if cleaned else cleaned


# --- State -----------------------------------------------------------------


@dataclass(slots=True)
class InterviewState:
    """Navigation state. Clinical facts live in the medical profile, not here."""

    # question id -> the normalised answer we accepted
    answers: dict[str, str] = field(default_factory=dict)
    # questions that are finished with (answered, or given up on)
    settled: list[str] = field(default_factory=list)
    # templated follow-ups queued by an earlier answer, in order
    queue: list[dict] = field(default_factory=list)
    # unusable-answer counts, so a question is re-asked but not forever
    attempts: dict[str, int] = field(default_factory=dict)
    # sections the patient has opted into (AYUSH is opt-in)
    enabled_sections: list[str] = field(default_factory=list)
    current_section: str = SECTION_ORDER[0]
    current_question_id: str | None = None
    # Follow-ups an AI suggested and the engine accepted, kept for audit.
    ai_follow_ups: list[dict[str, str]] = field(default_factory=list)
    # Which script this session walks: "profile" or "encounter".
    script_name: str = "profile"

    def to_json(self) -> dict:
        return {
            "answers": self.answers,
            "settled": self.settled,
            "queue": self.queue,
            "attempts": self.attempts,
            "enabled_sections": self.enabled_sections,
            "current_section": self.current_section,
            "current_question_id": self.current_question_id,
            "ai_follow_ups": self.ai_follow_ups,
            "script_name": self.script_name,
        }

    @classmethod
    def from_json(cls, raw: dict | None) -> "InterviewState":
        raw = raw or {}
        return cls(
            answers=dict(raw.get("answers") or {}),
            settled=list(raw.get("settled") or []),
            queue=list(raw.get("queue") or []),
            attempts=dict(raw.get("attempts") or {}),
            enabled_sections=list(raw.get("enabled_sections") or []),
            current_section=raw.get("current_section") or SECTION_ORDER[0],
            current_question_id=raw.get("current_question_id"),
            ai_follow_ups=list(raw.get("ai_follow_ups") or []),
            script_name=raw.get("script_name") or "profile",
        )


MAX_ATTEMPTS = 2


@dataclass(frozen=True, slots=True)
class Scheduled:
    """The next thing to ask, with any templated substitution applied."""

    question: Question
    # Non-empty when this is a per-item follow-up, e.g. "diabetes".
    item: str = ""
    # Unique per (question, item) so the same template can be asked twice.
    instance_id: str = ""
    # Set for an AI-suggested follow-up: the text and the section it feeds.
    prompt_override: dict[str, str] | None = None
    target_override: str | None = None

    @property
    def key(self) -> str:
        return self.instance_id or self.question.id

    @property
    def target(self) -> str | None:
        return self.target_override or self.question.target

    def prompt(self, language: str, easy: bool) -> str:
        if self.prompt_override:
            return render(localise(self.prompt_override, language), self.item)
        source = (
            self.question.easy_prompt
            if easy and self.question.easy_prompt
            else self.question.prompt
        )
        return render(localise(source, language), self.item)

    def help_text(self, language: str) -> str:
        return render(localise(self.question.help, language), self.item)


def instance_key(question_id: str, item: str = "") -> str:
    return f"{question_id}::{item}" if item else question_id


def enqueue_suggested(
    state: InterviewState, *, prompt: dict[str, str], target: str, tag: str
) -> bool:
    """Queue an AI-suggested follow-up.

    Returns False when it is rejected — the engine, not the model, decides
    whether a suggestion is asked at all. A suggestion is only accepted when
    it is new and the queue is not already crowded, which bounds how far a
    model can stretch the interview.
    """
    if len([entry for entry in state.queue if entry["question_id"] == "q_ai_follow_up"]) >= 2:
        return False
    key = instance_key("q_ai_follow_up", tag)
    if key in state.settled or any(
        instance_key(e["question_id"], e.get("item", "")) == key for e in state.queue
    ):
        return False
    state.queue.append(
        {"question_id": "q_ai_follow_up", "item": tag, "prompt": prompt, "target": target}
    )
    state.ai_follow_ups.append({"tag": tag, "target": target, **prompt})
    return True


def render(text: str, item: str) -> str:
    return text.replace("{item}", item) if item else text.replace(" for {item}", "").replace("{item}", "")


# --- Scheduling ------------------------------------------------------------


def _applicable(question: Question, state: InterviewState, item: str) -> bool:
    if question.when is None:
        return True
    # A per-item follow-up's gate reads the same item's answer, not the base.
    if item:
        scoped = {
            base_id: state.answers.get(instance_key(base_id, item), "")
            for base_id in [question.id, *_gate_ids(question)]
        }
        return question.when(scoped)
    return question.when(state.answers)


def _gate_ids(question: Question) -> list[str]:
    """Question ids a gate may read. Kept explicit rather than introspecting."""
    return ["q_condition_medicine", "q_has_conditions", "q_has_surgery", "q_has_investigations"]


def active_sections(state: InterviewState, script: Script = PROFILE_SCRIPT) -> list[str]:
    by_key = script.sections_by_key()
    return [
        key
        for key in script.section_order
        if not by_key[key].optional or key in state.enabled_sections
    ]


def next_question(
    state: InterviewState, script: Script = PROFILE_SCRIPT
) -> Scheduled | None:
    """The next question, or None when the interview is complete.

    Order: queued per-item follow-ups first (so a branch finishes before we
    move on), then the remaining questions of the current section, then later
    sections.
    """
    # 1. Queued follow-ups from an earlier answer.
    for entry in list(state.queue):
        question = script.question_by_id(entry["question_id"])
        if question is None:
            continue
        item = entry.get("item", "")
        key = instance_key(question.id, item)
        if key in state.settled:
            continue
        if not _applicable(question, state, item):
            state.settled.append(key)
            continue
        return Scheduled(
            question=question,
            item=item,
            instance_id=key,
            prompt_override=entry.get("prompt") if isinstance(entry.get("prompt"), dict) else None,
            target_override=entry.get("target"),
        )

    # 2. Walk sections in order from the current one.
    sections = active_sections(state, script)
    start = sections.index(state.current_section) if state.current_section in sections else 0
    for section in sections[start:]:
        for question in script.base_questions_for(section):
            if question.id in state.settled:
                continue
            if not _applicable(question, state, ""):
                state.settled.append(question.id)
                continue
            return Scheduled(question=question, instance_id=question.id)
    return None


# --- Applying an answer ----------------------------------------------------


@dataclass(frozen=True, slots=True)
class AppliedAnswer:
    """What the engine made of one answer."""

    # What the patient reads back on the review screen, in their language.
    stored: str
    # What logic branches on: the option's machine value, or the same text as
    # `stored` when the question had no options. Never localised.
    machine: str
    # Clinical items to write to `question.target`, already de-duplicated.
    # These carry the option labels, so the record reads in the patient's
    # language.
    items: list[str]
    # The same items as machine values, for anything that has to match a
    # controlled vocabulary (the AYUSH assessment) rather than display them.
    machine_items: list[str]
    # True when the answer could not be used and should be asked again.
    retry: bool
    # Per-item follow-ups this answer queued.
    queued: list[dict]


def apply_answer(
    state: InterviewState,
    scheduled: Scheduled,
    raw_answer: str,
    language: Language | str = Language.ENGLISH,
) -> AppliedAnswer:
    """Fold one answer into the state. Never raises on bad input.

    For a choice question the client sends the option's machine value, so the
    clinical record would otherwise read in English no matter which language
    the patient was answering in. The label the patient actually read is
    resolved here; the machine value stays in `state.answers` for the gates.
    """
    question = scheduled.question
    key = scheduled.key
    text = normalize(raw_answer)
    # Machine value -> the words the patient read.
    option_labels = {
        option.value.strip().lower(): localise(option.label, language)
        for option in question.options
        if option.value
    }

    # --- unusable answer -> re-ask, up to a limit ------------------------
    unusable = not text or (is_negative(text) and not question.allow_none and question.required)
    if unusable:
        attempts = state.attempts.get(key, 0) + 1
        state.attempts[key] = attempts
        if attempts < MAX_ATTEMPTS:
            return AppliedAnswer(stored="", machine="", items=[], machine_items=[], retry=True, queued=[])
        # Give up gracefully rather than trapping the patient.
        state.settled.append(key)
        _dequeue(state, key)
        return AppliedAnswer(stored="", machine="", items=[], machine_items=[], retry=False, queued=[])

    # --- yes/no gates carry no clinical value ----------------------------
    if question.kind == AnswerKind.YES_NO:
        stored = "yes" if is_affirmative(text) or not is_negative(text) else "no"
        if is_negative(text):
            stored = "no"
        state.answers[key] = stored
        state.settled.append(key)
        _dequeue(state, key)
        return AppliedAnswer(
            stored=stored,
            machine=stored,
            items=[],
            machine_items=[],
            retry=False,
            queued=[],
        )

    # --- everything else produces clinical items -------------------------
    # `items` are what the patient reads back; `machine` is what the gates
    # branch on. They differ only where an option label was resolved.
    if is_negative(text):
        items = [NONE_REPORTED]
        machine = list(items)
    elif question.kind == AnswerKind.SCALE:
        digits = re.sub(r"\D", "", text)
        items = [f"{digits or text}/10"]
        machine = list(items)
    else:
        tokens = (
            split_list(text)
            if question.kind in (AnswerKind.LIST, AnswerKind.MULTI_CHOICE)
            else [text]
        )
        items, machine = [], []
        for token in tokens:
            chosen = option_labels.get(token.strip().lower())
            items.append(chosen or sentence_case(token))
            machine.append(token.strip() if chosen else sentence_case(token))

    seen: set[str] = set()
    deduped: list[str] = []
    deduped_machine: list[str] = []
    for value, raw in zip(items, machine):
        marker = value.lower()
        if marker in seen or not value:
            continue
        seen.add(marker)
        deduped.append(value)
        deduped_machine.append(raw)

    state.answers[key] = ", ".join(deduped_machine)
    state.settled.append(key)
    _dequeue(state, key)

    # --- queue per-item follow-ups ---------------------------------------
    queued: list[dict] = []
    if question.per_item and deduped and deduped != [NONE_REPORTED]:
        for item in deduped:
            for template_id in question.per_item:
                entry = {"question_id": template_id, "item": item}
                if entry not in state.queue:
                    state.queue.append(entry)
                    queued.append(entry)

    return AppliedAnswer(
        stored=", ".join(deduped),
        machine=state.answers[key],
        items=deduped,
        machine_items=deduped_machine,
        retry=False,
        queued=queued,
    )


def _dequeue(state: InterviewState, key: str) -> None:
    state.queue = [
        entry
        for entry in state.queue
        if instance_key(entry["question_id"], entry.get("item", "")) != key
    ]


def go_back(state: InterviewState, script: Script = PROFILE_SCRIPT) -> Scheduled | None:
    """Un-settle the most recent answered question so it can be changed."""
    while state.settled:
        key = state.settled.pop()
        question_id = key.split("::")[0]
        item = key.split("::")[1] if "::" in key else ""
        question = script.question_by_id(question_id)
        if question is None:
            continue
        state.answers.pop(key, None)
        state.attempts.pop(key, None)
        # Rewind the cursor too: the section walk starts at `current_section`,
        # so leaving it ahead would skip straight past the reopened question.
        state.current_section = question.section
        return Scheduled(question=question, item=item, instance_id=key)
    return None


# --- Progress --------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Progress:
    answered: int
    total: int
    percent: int
    section: str
    section_index: int
    section_count: int


def progress(state: InterviewState, script: Script = PROFILE_SCRIPT) -> Progress:
    sections = active_sections(state, script)
    # Base questions plus whatever branches this patient's answers opened.
    total = sum(len(script.base_questions_for(section)) for section in sections) + len(state.queue)
    answered = len([key for key in state.settled if key in state.answers])
    section = state.current_section if state.current_section in sections else sections[0]
    return Progress(
        answered=answered,
        total=max(total, answered),
        percent=round(answered / max(1, max(total, answered)) * 100),
        section=section,
        section_index=sections.index(section),
        section_count=len(sections),
    )
