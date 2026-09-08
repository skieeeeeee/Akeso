import { describe, expect, it } from "vitest";
import {
  ONBOARDING_STEPS,
  canVisit,
  stepIndexFor,
  stepIndexForPath,
  stepperItems,
} from "./steps";

describe("onboarding step map", () => {
  it("mirrors the backend sequence order", () => {
    expect(ONBOARDING_STEPS.map((step) => step.status)).toEqual([
      "abha_pending",
      "personal_info_pending",
      "assessment_pending",
      "preferences_pending",
      "consent_pending",
      "medical_profile_pending",
    ]);
  });

  it("labels every step in both languages", () => {
    for (const step of ONBOARDING_STEPS) {
      expect(step.label.en).toBeTruthy();
      expect(step.label.hi).toBeTruthy();
    }
    expect(stepperItems("hi")).toHaveLength(ONBOARDING_STEPS.length);
  });

  it("places a completed patient past the last step", () => {
    expect(stepIndexFor("completed")).toBe(ONBOARDING_STEPS.length);
    expect(stepIndexFor("abha_pending")).toBe(0);
    expect(stepIndexFor("consent_pending")).toBe(4);
  });

  it("maps a path back to its step", () => {
    expect(stepIndexForPath("/onboarding/assessment")).toBe(2);
    expect(stepIndexForPath("/profile")).toBe(-1);
  });
});

describe("progress guard", () => {
  it("lets a patient revisit a finished step", () => {
    expect(canVisit("consent_pending", "/onboarding/abha")).toBe(true);
    expect(canVisit("consent_pending", "/onboarding/personal")).toBe(true);
  });

  it("blocks jumping ahead of recorded progress", () => {
    expect(canVisit("abha_pending", "/onboarding/consent")).toBe(false);
    expect(canVisit("personal_info_pending", "/onboarding/medical-profile")).toBe(false);
  });

  it("allows the step the patient is currently on", () => {
    expect(canVisit("assessment_pending", "/onboarding/assessment")).toBe(true);
  });

  it("lets a completed patient revisit anything", () => {
    for (const step of ONBOARDING_STEPS) {
      expect(canVisit("completed", step.path)).toBe(true);
    }
  });

  it("does not guard non-onboarding routes", () => {
    expect(canVisit("abha_pending", "/profile")).toBe(true);
  });
});
