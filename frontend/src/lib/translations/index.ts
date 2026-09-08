/**
 * Regional-language translations, one file per language.
 *
 * Kept apart from `strings.ts` on purpose: these were authored after the fact
 * and need review by a speaker of each language, which is only practical if
 * they sit in one flat file per language rather than as a sixth key on every
 * one of four hundred entries.
 *
 * Keyed by the English source string — that is what a reviewer reads, and the
 * same English string always means the same thing here. An explicit key in
 * `STRINGS` always wins, so an overlay entry can be corrected in place.
 */
import type { Language } from "@/types/api";
import { GUJARATI } from "./gu";
import { MARATHI } from "./mr";
import { PUNJABI } from "./pa";
import { TAMIL } from "./ta";

export const OVERLAYS: Partial<Record<Language, Record<string, string>>> = {
  mr: MARATHI,
  ta: TAMIL,
  gu: GUJARATI,
  pa: PUNJABI,
};

/** The overlay translation for an English source string, if there is one. */
export function overlay(english: string, language: Language): string | undefined {
  return OVERLAYS[language]?.[english];
}
