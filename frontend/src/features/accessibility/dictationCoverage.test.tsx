import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

/**
 * Every free-text field in the product must offer dictation.
 *
 * The interview had a microphone from the start and nothing else did, so a
 * patient who can speak but not type could describe their symptoms and then
 * be stopped at their own name. This reads the pages themselves rather than
 * rendering them, because the failure it guards is a field being *added*
 * later without a microphone — a render test only covers the fields that
 * already exist.
 *
 * Numeric fields are deliberately excluded: dictated digits are the least
 * reliable output speech recognition produces, and a wrong date of birth or
 * phone number is silent. Those are listed here so leaving them out stays a
 * decision on the record rather than an oversight.
 */

const SRC = resolve(__dirname, "../..");

const read = (relative: string) => readFileSync(resolve(SRC, relative), "utf8");

/** Pages holding at least one free-text field a patient fills in. */
const PAGES_WITH_FREE_TEXT = [
  "pages/PersonalInfoPage.tsx",
  "pages/MedicalProfilePage.tsx",
  "pages/AyushPage.tsx",
  "pages/RecordsPage.tsx",
];

/** Numeric-only, dictation deliberately withheld. */
const KEYPAD_ONLY = [
  ["pages/AbhaPage.tsx", "an ABHA number"],
  ["pages/LoginPage.tsx", "a mobile number"],
] as const;

describe("dictation coverage", () => {
  it.each(PAGES_WITH_FREE_TEXT)("%s offers dictation", (page) => {
    const source = read(page);
    expect(source).toContain("@/components/ui/Dictate");
    expect(source).toMatch(/<Dictate\b/);
  });

  it("covers every free-text field on the personal details page", () => {
    // Full name, emergency contact name, relationship. The date of birth and
    // the contact number are keypads on purpose.
    const source = read("pages/PersonalInfoPage.tsx");
    expect(source.match(/<Dictate\b/g)).toHaveLength(3);
  });

  it.each(KEYPAD_ONLY)("%s stays a keypad (%s)", (page) => {
    expect(read(page)).not.toMatch(/<Dictate\b/);
  });

  it("the interview keeps its own richer voice flow", () => {
    // AnswerInput has a confirm-what-we-heard step that a one-line field does
    // not need, so it uses the hook directly rather than this control.
    const source = read("features/interview/AnswerInput.tsx");
    expect(source).toContain("useVoiceInput");
  });

  it("dictation availability is never tied to a patient's touch preference", () => {
    // It once was: `interaction_preference !== "touch"` removed the microphone
    // outright, including for the demo patient most people open first.
    const source = read("features/interview/AnswerInput.tsx");
    expect(source).toMatch(/voiceAvailable\s*=\s*voice\.isSupported/);
    // Prominence may depend on the preference; availability may not.
    expect(source).not.toMatch(/voiceAvailable\s*=[^;]*interaction_preference/);
  });
});
