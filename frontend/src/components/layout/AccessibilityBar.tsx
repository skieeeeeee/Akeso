import { useMutation } from "@tanstack/react-query";
import { Contrast, Languages, Type } from "lucide-react";
import { api } from "@/services/apiClient";
import { Button } from "@/components/ui/Button";
import { LANGUAGE_LABELS, useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { useAuth } from "@/providers/AuthProvider";
import type { FontSize, Language, Preferences, PreferencesPayload } from "@/types/api";

const NEXT_FONT_SIZE: Record<FontSize, FontSize> = {
  normal: "large",
  large: "extra_large",
  extra_large: "normal",
};

/**
 * Always-available accessibility controls.
 *
 * Present on every screen including the welcome page, so a patient who cannot
 * read the current text size can fix that before doing anything else. When
 * signed in the change is persisted; before sign-in it applies locally.
 */
export function AccessibilityBar() {
  const { language, setLanguage, supported, t, v } = useI18n();
  const { preferences, preview, invalidate } = usePreferences();
  const { status } = useAuth();
  const isSignedIn = status === "signed_in";

  const save = useMutation({
    mutationFn: (payload: PreferencesPayload) =>
      api.put<Preferences>("/accessibility/preferences", payload),
    onSuccess: invalidate,
  });

  const apply = (partial: Partial<Preferences>) => {
    preview({ ...partial });
    if (isSignedIn) {
      save.mutate({ ...partial, accepted_recommendation: false } as PreferencesPayload);
    }
  };

  return (
    <div className="flex items-center gap-1.5">
      <Button
        variant="ghost"
        size="icon"
        onClick={() => apply({ font_size: NEXT_FONT_SIZE[preferences.font_size] })}
        aria-label={`${t("accessibilityShortcut")} (${v(preferences.font_size)})`}
        title={t("accessibilityShortcut")}
      >
        <Type className="h-5 w-5" aria-hidden="true" />
      </Button>

      <Button
        variant="ghost"
        size="icon"
        onClick={() =>
          apply({ contrast_mode: preferences.contrast_mode === "high" ? "normal" : "high" })
        }
        aria-label={t("contrastLabel")}
        aria-pressed={preferences.contrast_mode === "high"}
        title={t("contrastLabel")}
      >
        <Contrast className="h-5 w-5" aria-hidden="true" />
      </Button>

      {/* A native select: with six languages, cycling would take six taps,
          and this stays keyboard- and screen-reader-friendly for free. */}
      <label className="relative inline-flex min-h-touch items-center gap-1.5 rounded-xl px-2 text-ink-muted hover:bg-surface-muted">
        <Languages className="h-5 w-5" aria-hidden="true" />
        <span className="sr-only">{t("chooseLanguage")}</span>
        <select
          value={language}
          onChange={(event) => {
            const next = event.target.value as Language;
            setLanguage(next);
            if (isSignedIn) apply({ language: next });
          }}
          className="cursor-pointer appearance-none bg-transparent py-2 pr-1 text-sm font-semibold text-ink focus:outline-none"
        >
          {supported.map((code) => (
            <option key={code} value={code}>
              {LANGUAGE_LABELS[code].native}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
