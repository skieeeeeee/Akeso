import { describe, expect, it } from "vitest";
import {
  ENUM_LABELS,
  enumLabel,
  sourceSentence,
  untranslatedLabels,
  type EnumValue,
} from "./enumLabels";

const KEYS = Object.keys(ENUM_LABELS) as EnumValue[];

describe("enum labels", () => {
  it("Hindi covers every value the API can send", () => {
    // A gap here is what makes a Hindi page show "needs_review" in English.
    expect(untranslatedLabels("hi")).toEqual([]);
  });

  it("resolves in every language through the fallback chain", () => {
    for (const language of ["en", "hi", "mr", "ta", "gu", "pa"] as const) {
      for (const key of KEYS) {
        expect(enumLabel(key, language), `${key} / ${language}`).toBeTruthy();
      }
    }
  });

  it("shows an unmapped value as a readable slug rather than nothing", () => {
    // A new backend enum value must degrade visibly, so the gap gets noticed.
    expect(enumLabel("some_new_status", "hi")).toBe("some new status");
    expect(enumLabel(null, "hi")).toBe("");
  });

  it("never leaves an underscore on screen", () => {
    for (const key of KEYS) {
      expect(enumLabel(key, "en"), key).not.toMatch(/_/);
      expect(enumLabel(key, "hi"), key).not.toMatch(/_/);
    }
  });

  it("composes the document provenance sentence in the chosen language", () => {
    expect(sourceSentence("found_in_document", "City Lab", "en")).toBe("Found in City Lab");
    expect(sourceSentence("found_in_document", "City Lab", "hi")).toBe("City Lab में मिला");
    expect(sourceSentence("visit_record", "", "hi")).toBe("मुलाक़ात का रिकॉर्ड");
  });

  it("keeps Hindi labels free of Latin script", () => {
    // Catches a value that was added with the English text copied into `hi`.
    for (const key of KEYS) {
      expect(enumLabel(key, "hi"), key).not.toMatch(/[A-Za-z]/);
    }
  });
});
