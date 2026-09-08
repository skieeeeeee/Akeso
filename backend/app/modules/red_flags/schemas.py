"""Red-flag API contracts.

What crosses the boundary: a category, patient-safe guidance, and the
patient's own words. What never crosses it: the criteria that fired.
"""

from __future__ import annotations

from datetime import datetime

from app.shared.enums import RedFlagCategory, RedFlagSource, RedFlagStatus
from app.shared.schemas import ApiModel


class RedFlagOut(ApiModel):
    category: RedFlagCategory
    source: RedFlagSource
    # Quoted from the patient, so they recognise what prompted this.
    evidence: str
    created_at: datetime


class SafetyNotice(ApiModel):
    """The emergency screen's content, in both languages."""

    title: dict[str, str]
    body: dict[str, str]
    # Explicitly states this is not a diagnosis.
    disclaimer: dict[str, str]
    action_staff: dict[str, str]
    action_continue: dict[str, str]
    # What the patient should do right now.
    instruction: dict[str, str]


class RedFlagStateOut(ApiModel):
    status: RedFlagStatus
    flags: list[RedFlagOut]
    # Present only while status is active.
    notice: SafetyNotice | None
    # True once the patient has seen the emergency screen.
    acknowledged: bool
    # Always false for a patient — priority is not theirs to change.
    can_be_cleared_by_patient: bool = False
