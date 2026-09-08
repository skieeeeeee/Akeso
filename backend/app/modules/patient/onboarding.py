"""Onboarding progression rules.

The patient's `onboarding_status` is the single source of truth for where they
are in the first-time journey, so a refresh, a back button or a new device all
resume at the same place. Steps only ever move forward — revisiting a finished
step never rewinds the journey.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.shared.i18n import Localised, t
from app.shared.enums import ONBOARDING_SEQUENCE, OnboardingStatus

# Frontend route for each pending stage. Kept server-side so routing after
# login cannot disagree with the persisted state.
STEP_ROUTES: dict[OnboardingStatus, str] = {
    OnboardingStatus.ABHA_PENDING: "/onboarding/abha",
    OnboardingStatus.PERSONAL_INFO_PENDING: "/onboarding/personal",
    OnboardingStatus.ASSESSMENT_PENDING: "/onboarding/assessment",
    OnboardingStatus.PREFERENCES_PENDING: "/onboarding/preferences",
    OnboardingStatus.CONSENT_PENDING: "/onboarding/consent",
    OnboardingStatus.MEDICAL_PROFILE_PENDING: "/onboarding/medical-profile",
    OnboardingStatus.COMPLETED: "/profile",
}

STEP_LABELS: dict[OnboardingStatus, Localised] = {
    OnboardingStatus.ABHA_PENDING: t("Health ID", "हेल्थ आईडी"),
    OnboardingStatus.PERSONAL_INFO_PENDING: t("Your details", "आपकी जानकारी"),
    OnboardingStatus.ASSESSMENT_PENDING: t("Comfort check", "सुविधा जाँच"),
    OnboardingStatus.PREFERENCES_PENDING: t("Your experience", "आपका अनुभव"),
    OnboardingStatus.CONSENT_PENDING: t("Consent", "सहमति"),
    OnboardingStatus.MEDICAL_PROFILE_PENDING: t("Health history", "स्वास्थ्य इतिहास"),
    OnboardingStatus.COMPLETED: t("Done", "पूर्ण"),
}


def step_index(status: OnboardingStatus) -> int:
    return ONBOARDING_SEQUENCE.index(status)


def is_at_or_past(status: OnboardingStatus, target: OnboardingStatus) -> bool:
    return step_index(status) >= step_index(target)


def advance(current: OnboardingStatus, completed: OnboardingStatus) -> OnboardingStatus:
    """Status after finishing `completed`.

    Never moves the patient backwards: a patient who edits an earlier step
    keeps whatever later progress they already had.
    """
    if is_at_or_past(current, OnboardingStatus.COMPLETED):
        return OnboardingStatus.COMPLETED
    following = ONBOARDING_SEQUENCE[min(step_index(completed) + 1, len(ONBOARDING_SEQUENCE) - 1)]
    return following if step_index(following) > step_index(current) else current


@dataclass(frozen=True, slots=True)
class OnboardingProgress:
    status: OnboardingStatus
    step_number: int
    total_steps: int
    percent: int
    next_route: str
    is_complete: bool


def progress_for(status: OnboardingStatus) -> OnboardingProgress:
    # The final COMPLETED entry is a destination, not a step to perform.
    total = len(ONBOARDING_SEQUENCE) - 1
    index = step_index(status)
    return OnboardingProgress(
        status=status,
        step_number=min(index + 1, total),
        total_steps=total,
        percent=round(min(index, total) / total * 100),
        next_route=STEP_ROUTES[status],
        is_complete=status == OnboardingStatus.COMPLETED,
    )
