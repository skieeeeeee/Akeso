import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { localised } from "@/services/apiClient";
import { loadOverlay, overlayReady } from "@/lib/translations";
import { translate, type StringKey } from "@/lib/strings";
import { enumLabel } from "@/lib/enumLabels";
import type { Language, Localised } from "@/types/api";

const STORAGE_KEY = "medikiosk.language";
const SUPPORTED: Language[] = ["en", "hi", "mr", "ta", "gu", "pa"];

/**
 * Each language named in its own script, which is how a speaker recognises
 * it. `english` is a gloss for a reader of English only — showing it beside
 * the native name in a Hindi interface just puts English back on the screen,
 * so the settings page drops it unless the interface is in English.
 */
export const LANGUAGE_LABELS: Record<Language, { native: string; english: string }> = {
  en: { native: "English", english: "English" },
  hi: { native: "हिन्दी", english: "Hindi" },
  mr: { native: "मराठी", english: "Marathi" },
  ta: { native: "தமிழ்", english: "Tamil" },
  gu: { native: "ગુજરાતી", english: "Gujarati" },
  pa: { native: "ਪੰਜਾਬੀ", english: "Punjabi" },
};

type I18nValue = {
  language: Language;
  setLanguage: (language: Language) => void;
  /** Static UI copy. */
  t: (key: StringKey) => string;
  /** Localised copy that came from the API. */
  s: (value: Localised | Record<string, string> | undefined) => string;
  /** The label for an API enum value, e.g. `needs_review`. */
  v: (value: string | null | undefined) => string;
  supported: Language[];
};

const I18nContext = createContext<I18nValue | null>(null);

function readStoredLanguage(): Language {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored && SUPPORTED.includes(stored as Language)) return stored as Language;
  } catch {
    /* private mode */
  }
  // Fall back to the browser's preference before defaulting to English.
  const browser = (typeof navigator !== "undefined" ? navigator.language : "").slice(0, 2);
  return SUPPORTED.includes(browser as Language) ? (browser as Language) : "en";
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>(readStoredLanguage);
  // Bumped when a translation file finishes loading, so the tree re-renders
  // with it. `overlay` is read during render and cannot be awaited there.
  const [loaded, setLoaded] = useState(0);

  const setLanguage = useCallback((next: Language) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* preference simply will not persist */
    }
    // Switch only once the text for it is in hand, so choosing Marathi never
    // shows a frame of Hindi on the way.
    if (overlayReady(next)) {
      setLanguageState(next);
      return;
    }
    void loadOverlay(next).then(() => {
      setLanguageState(next);
      setLoaded((n) => n + 1);
    });
  }, []);

  // The stored or browser-detected language is known before anything renders,
  // so fetch its file immediately rather than waiting for a switch.
  useEffect(() => {
    if (overlayReady(language)) return;
    let cancelled = false;
    void loadOverlay(language).then(() => {
      if (!cancelled) setLoaded((n) => n + 1);
    });
    return () => {
      cancelled = true;
    };
  }, [language]);

  // `lang` drives font selection and screen-reader pronunciation.
  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  const value = useMemo<I18nValue>(
    () => ({
      language,
      setLanguage,
      t: (key) => translate(key, language),
      s: (record) => localised(record, language),
      v: (value) => enumLabel(value, language),
      supported: SUPPORTED,
    }),
    // `loaded` is in here on purpose. Without it the memo returns the same
    // object after a translation file arrives, so every consumer of the
    // context keeps the identical value and never re-renders — the text
    // stayed in the fallback language even though the overlay was in memory.
    [language, setLanguage, loaded],
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nValue {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useI18n must be used inside I18nProvider");
  return context;
}
