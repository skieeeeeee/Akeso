"""Red-flag evaluation.

Rules run first and are authoritative for raising a flag. The AI layer may
add a category the rules missed, bounded to the same enum, and can never
remove one. A patient-facing API can never lower the priority it sets.
"""

from __future__ import annotations

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.red_flags import rules
from app.modules.red_flags.content import SAFETY_NOTICE
from app.modules.red_flags.models import RedFlag
from app.modules.red_flags.schemas import RedFlagOut, RedFlagStateOut, SafetyNotice
from app.services.ai import get_provider, structured
from app.services.ai.schemas import Strict
from app.shared.enums import (
    EncounterPriority,
    RedFlagCategory,
    RedFlagSource,
    RedFlagStatus,
)
from pydantic import Field

log = logging.getLogger("medikiosk.red_flags")


class _AiConcern(Strict):
    """Bounded AI output: a category from our enum, nothing free-form."""

    category: RedFlagCategory
    quote: str = Field(min_length=1, max_length=240)


class _AiScreen(Strict):
    concerns: list[_AiConcern] = Field(default_factory=list, max_length=3)


async def _ai_screen(texts: list[str]) -> list[rules.RuleHit]:
    """Optional second opinion. Returns [] whenever unavailable."""
    provider = get_provider()
    if provider.name == "none" or not texts:
        return []

    system = (
        "You are a triage screening assistant for a hospital waiting room. "
        "You NEVER diagnose. Your only job is to say whether the patient's own "
        "words describe a presentation that a nurse should see sooner rather "
        "than later. Quote the patient verbatim; never paraphrase or infer. "
        "If nothing in the text is urgent, return an empty list. "
        "Respond with a single JSON object and nothing else."
    )
    prompt = (
        "Patient's answers from this visit:\n"
        + "\n".join(f"- {text}" for text in texts[:12])
        + "\n\nCategories: breathing, chest, bleeding, consciousness, "
        "neurological, other.\n"
        'Return {"concerns":[{"category","quote"}]}'
    )
    try:
        raw = await provider.complete_json(system=system, prompt=prompt, max_tokens=700)
    except Exception as exc:  # noqa: BLE001 - screening must never fail the visit
        log.warning("AI red-flag screen failed: %s", exc)
        return []

    parsed = structured(_AiScreen, raw)
    if parsed is None:
        return []
    return [
        rules.RuleHit(category=concern.category, evidence=concern.quote)
        for concern in parsed.concerns
    ]


async def evaluate(
    db: Session, encounter, texts: list[str], severity: str | None = None
) -> list[RedFlag]:
    """Screen this encounter and persist any new flags.

    Never lowers priority and never deletes a flag. Returns only the flags
    newly raised by this call.
    """
    score = rules.parse_severity(severity)
    hits = rules.evaluate(texts, score)
    sources = {hit.category: RedFlagSource.RULES for hit in hits}

    # The AI pass may add a category the rules did not catch.
    for hit in await _ai_screen(texts):
        if hit.category not in sources:
            hits.append(hit)
            sources[hit.category] = RedFlagSource.AI_ASSIST

    if not hits:
        return []

    existing = {
        flag.category
        for flag in db.scalars(
            select(RedFlag).where(RedFlag.encounter_id == encounter.id)
        ).all()
    }

    created: list[RedFlag] = []
    for hit in hits:
        if hit.category in existing:
            continue
        flag = RedFlag(
            encounter_id=encounter.id,
            category=hit.category,
            source=sources[hit.category],
            evidence=hit.evidence,
        )
        db.add(flag)
        created.append(flag)

    if created:
        # Priority only ever ratchets upward here.
        encounter.priority = EncounterPriority.URGENT
        encounter.red_flag_status = RedFlagStatus.ACTIVE
        db.flush()
        log.info(
            "encounter %s flagged: %s",
            encounter.id,
            [flag.category.value for flag in created],
        )
    return created


def list_for_encounter(db: Session, encounter_id: uuid.UUID) -> list[RedFlag]:
    return list(
        db.scalars(
            select(RedFlag)
            .where(RedFlag.encounter_id == encounter_id)
            .order_by(RedFlag.created_at)
        ).all()
    )


def state_for(db: Session, encounter) -> RedFlagStateOut:
    flags = list_for_encounter(db, encounter.id)
    active = encounter.red_flag_status == RedFlagStatus.ACTIVE
    return RedFlagStateOut(
        status=encounter.red_flag_status,
        flags=[RedFlagOut.model_validate(flag) for flag in flags],
        notice=SafetyNotice(**SAFETY_NOTICE) if active else None,
        acknowledged=encounter.red_flag_acknowledged_at is not None,
        can_be_cleared_by_patient=False,
    )
