/**
 * Regional-language translations, one file per language, loaded on demand.
 *
 * Kept apart from `strings.ts` on purpose: these were authored after the fact
 * and need review by a speaker of each language, which is only practical if
 * they sit in one flat file per language rather than as a sixth key on every
 * one of four hundred entries.
 *
 * Keyed by the English source string — that is what a reviewer reads, and the
 * same English string always means the same thing here. An explicit key in
 * `STRINGS` always wins, so an overlay entry can be corrected in place.
 *
 * Why they are imported dynamically: the four files are about 245 KB of
 * source between them, and every patient was downloading all four regardless
 * of which language they chose. An English or Hindi patient needs none of
 * them. On a mid-range phone over mobile data — which is who this product is
 * for — that was a wait before anything on screen was usable.
 *
 * `overlay` stays synchronous because it is called during render. Before the
 * file for a language has loaded it simply reports no translation, which
 * lands on the existing fallback chain (mr/gu/pa to Hindi, ta to English) —
 * so the worst case is correct text in the second-choice language, never a
 * blank or a key. `I18nProvider` loads the file before it switches language,
 * so in practice that window does not appear.
 */
import type { Language } from "@/types/api";

const OVERLAYS: Partial<Record<Language, Record<string, string>>> = {};

const LOADERS: Partial<Record<Language, () => Promise<Record<string, string>>>> = {
  mr: () => import("./mr").then((m) => m.MARATHI),
  ta: () => import("./ta").then((m) => m.TAMIL),
  gu: () => import("./gu").then((m) => m.GUJARATI),
  pa: () => import("./pa").then((m) => m.PUNJABI),
};

/** Languages whose text lives in an overlay file rather than inline. */
export const OVERLAID: Language[] = Object.keys(LOADERS) as Language[];

/** The overlay translation for an English source string, if there is one. */
export function overlay(english: string, language: Language): string | undefined {
  return OVERLAYS[language]?.[english];
}

/** True once this language needs no further loading. */
export function overlayReady(language: Language): boolean {
  return !(language in LOADERS) || OVERLAYS[language] !== undefined;
}

const inFlight = new Map<Language, Promise<void>>();

/**
 * Fetch the overlay for one language, at most once.
 *
 * @returns a promise that resolves when `overlay` can answer for it. Resolves
 *          immediately for English and Hindi, which are inline. A failed
 *          fetch resolves rather than rejects: losing a translation file must
 *          degrade to the fallback language, not break the page.
 */
export function loadOverlay(language: Language): Promise<void> {
  if (overlayReady(language)) return Promise.resolve();
  const existing = inFlight.get(language);
  if (existing) return existing;

  const load = LOADERS[language]!()
    .then((entries) => {
      OVERLAYS[language] = entries;
    })
    .catch(() => {
      // Leave it unloaded; `overlay` reports nothing and the chain takes over.
      inFlight.delete(language);
    });
  inFlight.set(language, load);
  return load;
}

/** Every overlay, for the tests that assert coverage across all six. */
export function loadAllOverlays(): Promise<void[]> {
  return Promise.all(OVERLAID.map(loadOverlay));
}
