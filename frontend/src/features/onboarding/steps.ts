/**
 * The onboarding journey, defined once.
 *
 * The order mirrors `ONBOARDING_SEQUENCE` in the backend. Routes, the step
 * indicator and the "can this patient be here yet?" guard all read from this
 * list, so they cannot disagree.
 */
import { localised } from "@/services/apiClient";
import type { Language, Localised, OnboardingStatus } from "@/types/api";

export type OnboardingStep = {
  status: OnboardingStatus;
  path: string;
  /** English required; other languages resolve via the fallback chain. */
  label: Localised;
};

export const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    status: "abha_pending",
    path: "/onboarding/abha",
    label: { en: "Health ID", hi: "हेल्थ आईडी" },
  },
  {
    status: "personal_info_pending",
    path: "/onboarding/personal",
    label: { en: "Your details", hi: "आपकी जानकारी" },
  },
  {
    status: "assessment_pending",
    path: "/onboarding/assessment",
    label: { en: "Comfort", hi: "सुविधा" },
  },
  {
    status: "preferences_pending",
    path: "/onboarding/preferences",
    label: { en: "Experience", hi: "अनुभव" },
  },
  {
    status: "consent_pending",
    path: "/onboarding/consent",
    label: { en: "Consent", hi: "सहमति" },
  },
  {
    status: "medical_profile_pending",
    path: "/onboarding/medical-profile",
    label: { en: "History", hi: "इतिहास" },
  },
];

/** Where a patient goes after the last step. */
export const PROFILE_PATH = "/profile";

/**
 * Where a recognised, fully-onboarded patient lands after signing in.
 *
 * The server returns `/profile` as its generic "you are done" route; the
 * client prefers the personalised home screen, which is the actual entry
 * point for a returning visit.
 */
export const HOME_PATH = "/home";

export function postLoginRoute(nextRoute: string, isComplete: boolean): string {
  return isComplete ? HOME_PATH : nextRoute;
}

export function stepIndexFor(status: OnboardingStatus): number {
  if (status === "completed") return ONBOARDING_STEPS.length;
  const index = ONBOARDING_STEPS.findIndex((step) => step.status === status);
  return index === -1 ? 0 : index;
}

export function stepIndexForPath(path: string): number {
  return ONBOARDING_STEPS.findIndex((step) => path.startsWith(step.path));
}

export function stepperItems(language: Language) {
  return ONBOARDING_STEPS.map((step) => ({
    key: step.status,
    label: localised(step.label, language),
  }));
}

/**
 * A patient may revisit a finished step, but may not jump ahead of where the
 * server says they are — the server's status is the authority.
 */
export function canVisit(status: OnboardingStatus, path: string): boolean {
  const target = stepIndexForPath(path);
  if (target === -1) return true;
  return target <= stepIndexFor(status);
}
