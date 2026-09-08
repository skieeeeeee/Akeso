import { describe, expect, it } from "vitest";
import { OVERLAYS } from "./index";
import { STRINGS, translate, untranslated, type StringKey } from "@/lib/strings";
import { ENUM_LABELS, enumLabel, untranslatedLabels } from "@/lib/enumLabels";
import { HEADLINE, STATISTICS } from "@/features/landing/statistics";
import { localised } from "@/services/apiClient";
import type { Language } from "@/types/api";

const REGIONAL: Language[] = ["mr", "ta", "gu", "pa"];

// Each script's Unicode block. Devanagari, Gujarati and Gurmukhi look similar
// enough that one letter typed from the wrong block is invisible on review but
// renders as a foreign glyph mid-word.
const BLOCKS: Record<string, [number, number]> = {
  mr: [0x0900, 0x097f],
  gu: [0x0a80, 0x0aff],
  pa: [0x0a00, 0x0a7f],
  ta: [0x0b80, 0x0bff],
};

describe("regional-language overlays", () => {
  it.each(REGIONAL)("%s covers every UI string", (language) => {
    expect(untranslated(language)).toEqual([]);
  });

  it.each(REGIONAL)("%s covers every enum label", (language) => {
    expect(untranslatedLabels(language)).toEqual([]);
  });

  it.each(REGIONAL)("%s resolves every key to something", (language) => {
    for (const key of Object.keys(STRINGS) as StringKey[]) {
      expect(translate(key, language), key).toBeTruthy();
    }
    for (const value of Object.keys(ENUM_LABELS)) {
      expect(enumLabel(value, language), value).toBeTruthy();
    }
  });

  it.each(REGIONAL)("%s covers the landing statistics", (language) => {
    // These live outside STRINGS and once had their own two-language helper,
    // which is why the figures stayed English on a Tamil landing page.
    for (const stat of [HEADLINE, ...STATISTICS]) {
      // `unit` is absent on statistics rendered as a bare number.
      for (const field of [stat.unit, stat.label, stat.detail]) {
        if (!field) continue;
        expect(field[language], `${stat.id} / ${language}`).toBeTruthy();
        expect(localised(field, language)).toBe(field[language]);
      }
    }
  });

  it.each(REGIONAL)("%s leaves no entry as its English source", (language) => {
    // An entry copied from English is worse than no entry: it defeats the
    // fallback chain and shows English under a regional key.
    const same = Object.entries(OVERLAYS[language]!).filter(
      ([english, text]) =>
        text.trim() === english.trim() &&
        english.replace(/\{\w+\}|[^A-Za-z ]/g, "").trim(),
    );
    expect(same.map(([english]) => english)).toEqual([]);
  });

  it.each(REGIONAL)("%s keeps every {placeholder}", (language) => {
    // A string that loses its {placeholder} renders the literal token to the
    // patient, or drops the value it was meant to carry.
    for (const [english, text] of Object.entries(OVERLAYS[language]!)) {
      const expected = [...english.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort();
      const actual = [...text.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort();
      expect(actual, english).toEqual(expected);
    }
  });

  it.each(REGIONAL)("%s is written in its own script", (language) => {
    const [low, high] = BLOCKS[language]!;
    const wrong: string[] = [];
    for (const [english, text] of Object.entries(OVERLAYS[language]!)) {
      for (const ch of text) {
        const point = ch.codePointAt(0)!;
        // Latin, digits, punctuation and spacing are all legitimate.
        if (point < 0x0900 || /[\s\p{P}\p{S}]/u.test(ch)) continue;
        if (point < low || point > high) {
          wrong.push(`${english}: ${ch} U+${point.toString(16).toUpperCase()}`);
        }
      }
    }
    expect(wrong).toEqual([]);
  });

  it("has no replacement characters", () => {
    // A U+FFFD means a character was mangled on the way into the file.
    for (const language of REGIONAL) {
      for (const [english, text] of Object.entries(OVERLAYS[language]!)) {
        expect(text.includes("�"), `${language} / ${english}`).toBe(false);
      }
    }
  });
});
