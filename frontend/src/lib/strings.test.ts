import { describe, expect, it } from "vitest";
import { STRINGS, translate, untranslated, type StringKey } from "./strings";
import { localised } from "@/services/apiClient";
import type { Language } from "@/types/api";

const LANGUAGES: Language[] = ["en", "hi", "mr", "ta", "gu", "pa"];
const KEYS = Object.keys(STRINGS) as StringKey[];

describe("UI strings", () => {
  it("every key has English", () => {
    for (const key of KEYS) {
      expect(STRINGS[key].en, key).toBeTruthy();
    }
  });

  it("every key resolves to something in every language", () => {
    // The fallback chain means a missing translation degrades, never blanks.
    for (const language of LANGUAGES) {
      for (const key of KEYS) {
        expect(translate(key, language), `${key} / ${language}`).toBeTruthy();
      }
    }
  });

  it("Hindi is fully translated", () => {
    // Hindi is the fallback for every regional language, so a gap here
    // silently degrades four other languages to English.
    expect(untranslated("hi")).toEqual([]);
  });

  it("reports coverage per language so gaps are visible, not hidden", () => {
    const coverage = LANGUAGES.map((language) => ({
      language,
      translated: KEYS.length - untranslated(language).length,
      total: KEYS.length,
    }));
    // All six are now complete: English and Hindi inline, the regional four
    // through the overlay files. If a new string is added without a
    // translation, this is the test that says so.
    for (const entry of coverage) {
      expect(entry.translated, entry.language).toBe(entry.total);
    }
  });
});

describe("fallback chain", () => {
  it("prefers the exact language", () => {
    expect(localised({ en: "Fever", hi: "बुखार", mr: "ताप" }, "mr")).toBe("ताप");
  });

  it("falls back to Hindi for a Devanagari-reading language", () => {
    // Marathi is written in Devanagari; Hindi is widely read in Gujarat and
    // Punjab too, so Hindi is a real second choice for these three.
    for (const language of ["mr", "gu", "pa"] as const) {
      expect(localised({ en: "Fever", hi: "बुखार" }, language)).toBe("बुखार");
    }
  });

  it("falls back to English for Tamil, not Hindi", () => {
    // Devanagari is not read in Tamil Nadu, so Hindi would be no more useful
    // to a Tamil patient than a blank.
    expect(localised({ en: "Fever", hi: "बुखार" }, "ta")).toBe("Fever");
  });

  it("falls back to English when there is no Hindi", () => {
    expect(localised({ en: "Fever" }, "gu")).toBe("Fever");
  });

  it("never resolves English to another language", () => {
    expect(localised({ en: "Fever", hi: "बुखार" }, "en")).toBe("Fever");
  });

  it("returns empty rather than undefined for a missing value", () => {
    expect(localised(undefined, "hi")).toBe("");
    expect(localised({} as never, "hi")).toBe("");
  });

  it("mirrors the server chain for every language", () => {
    for (const language of LANGUAGES) {
      expect(localised({ en: "only english" }, language)).toBe("only english");
    }
  });
});
