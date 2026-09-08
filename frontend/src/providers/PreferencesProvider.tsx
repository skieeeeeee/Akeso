import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api } from "@/services/apiClient";
import { useAuth } from "./AuthProvider";
import { useI18n } from "./I18nProvider";
import type { Preferences } from "@/types/api";

/**
 * Applies the patient's accessibility settings to the document root.
 *
 * Every component then inherits the right text size, contrast and spacing
 * without knowing that modes exist — which is what stops Easy Mode from
 * becoming a second copy of the UI.
 */

export const DEFAULT_PREFERENCES: Preferences = {
  interface_mode: "standard",
  font_size: "normal",
  contrast_mode: "normal",
  audio_guidance: false,
  interaction_preference: "touch",
  language: "en",
  source: "recommended",
  updated_at: null,
};

type PreferencesValue = {
  preferences: Preferences;
  isEasyMode: boolean;
  isLoading: boolean;
  /** Apply settings locally without saving — used for live previews. */
  preview: (partial: Partial<Preferences> | null) => void;
  /** Re-read from the server after a save. */
  invalidate: () => void;
};

const PreferencesContext = createContext<PreferencesValue | null>(null);
export const PREFERENCES_QUERY_KEY = ["preferences"] as const;

export function PreferencesProvider({ children }: { children: ReactNode }) {
  const { status } = useAuth();
  const { language, setLanguage } = useI18n();
  const queryClient = useQueryClient();
  const [previewOverride, setPreviewOverride] = useState<Partial<Preferences> | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: PREFERENCES_QUERY_KEY,
    queryFn: () => api.get<Preferences>("/accessibility/preferences"),
    enabled: status === "signed_in",
    staleTime: 30_000,
  });

  const preferences = useMemo<Preferences>(() => {
    const base = data ?? { ...DEFAULT_PREFERENCES, language };
    return previewOverride ? { ...base, ...previewOverride } : base;
  }, [data, previewOverride, language]);

  // The server is the source of truth for language once signed in.
  useEffect(() => {
    if (data && data.language !== language) setLanguage(data.language);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- react to server value only
  }, [data?.language]);

  // Apply to <html> so CSS custom properties and rem scaling take effect.
  useEffect(() => {
    const root = document.documentElement;
    root.dataset.fontSize = preferences.font_size;
    root.dataset.contrast = preferences.contrast_mode;
    root.dataset.mode = preferences.interface_mode;
  }, [preferences.font_size, preferences.contrast_mode, preferences.interface_mode]);

  const invalidate = useCallback(() => {
    setPreviewOverride(null);
    void queryClient.invalidateQueries({ queryKey: PREFERENCES_QUERY_KEY });
  }, [queryClient]);

  const value = useMemo<PreferencesValue>(
    () => ({
      preferences,
      isEasyMode: preferences.interface_mode === "easy",
      // Also "loading" while auth is still restoring. Otherwise the
      // preferences query only becomes enabled *after* restoration, so a page
      // renders its content, then flips back to a loading panel — a visible
      // flash, and a race for anything reading preferences.
      isLoading: status === "restoring" || (status === "signed_in" && isLoading),
      preview: setPreviewOverride,
      invalidate,
    }),
    [preferences, isLoading, status, invalidate],
  );

  return (
    <PreferencesContext.Provider value={value}>{children}</PreferencesContext.Provider>
  );
}

export function usePreferences(): PreferencesValue {
  const context = useContext(PreferencesContext);
  if (!context) throw new Error("usePreferences must be used inside PreferencesProvider");
  return context;
}
