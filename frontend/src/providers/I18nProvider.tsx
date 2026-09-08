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

  const setLanguage = useCallback((next: Language) => {
    setLanguageState(next);
    try {
      window.localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* preference simply will not persist */
    }
  }, []);

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
    [language, setLanguage],
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nValue {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useI18n must be used inside I18nProvider");
  return context;
}
