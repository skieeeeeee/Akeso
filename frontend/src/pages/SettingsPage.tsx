import { useMutation, useQuery } from "@tanstack/react-query";
import * as SwitchPrimitive from "@radix-ui/react-switch";
import { CheckCircle2, Languages, RotateCcw, Settings2 } from "lucide-react";
import { Link } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { LANGUAGE_LABELS, useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import type {
  AssessmentContent,
  ContrastMode,
  FontSize,
  InteractionPreference,
  InterfaceMode,
  Language,
  Preferences,
  PreferencesPayload,
} from "@/types/api";

const GROUP_LABELS = {
  interface_mode: "interfaceModeLabel",
  font_size: "fontSizeLabel",
  contrast_mode: "contrastLabel",
  interaction_preference: "interactionLabel",
} as const;

/**
 * Settings.
 *
 * Every change is applied immediately (so the effect is visible) and saved
 * server-side. Retaking the accessibility assessment is offered but never
 * required — the patient is not made to repeat it to adjust one setting.
 */
export function SettingsPage() {
  const { t, s, language, setLanguage } = useI18n();
  const { preferences, preview, invalidate, isEasyMode, isLoading } = usePreferences();

  const content = useQuery({
    queryKey: ["assessment-content"],
    queryFn: () => api.get<AssessmentContent>("/accessibility/content"),
    staleTime: Infinity,
  });

  const save = useMutation({
    mutationFn: (payload: PreferencesPayload) =>
      api.put<Preferences>("/accessibility/preferences", payload),
    onSuccess: invalidate,
  });

  /** Apply locally for instant feedback, then persist. */
  const change = <K extends keyof Preferences>(key: K, value: Preferences[K]) => {
    preview({ [key]: value } as Partial<Preferences>);
    save.mutate({ [key]: value, accepted_recommendation: false } as PreferencesPayload);
  };

  if (isLoading || content.isLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  const options = content.data?.preference_options ?? {};
  const groups: Array<{ key: keyof typeof GROUP_LABELS; current: string; onSelect: (value: string) => void }> = [
    {
      key: "interface_mode",
      current: preferences.interface_mode,
      onSelect: (value) => change("interface_mode", value as InterfaceMode),
    },
    {
      key: "font_size",
      current: preferences.font_size,
      onSelect: (value) => change("font_size", value as FontSize),
    },
    {
      key: "contrast_mode",
      current: preferences.contrast_mode,
      onSelect: (value) => change("contrast_mode", value as ContrastMode),
    },
    {
      key: "interaction_preference",
      current: preferences.interaction_preference,
      onSelect: (value) => change("interaction_preference", value as InteractionPreference),
    },
  ];

  return (
    <AppShell wide backRoute="/home" backLabel={t("backToHome")}>
      <div className="space-y-5">
        <div>
          <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("settingsHeading")}</h1>
          <p className="mt-1 text-base text-ink-muted">{t("settingsBody")}</p>
        </div>

        {save.isSuccess && (
          <Alert tone="success">
            <span className="inline-flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5" aria-hidden="true" />
              {t("settingsSaved")}
            </span>
          </Alert>
        )}
        {save.error && (
          <Alert tone="danger">
            {save.error instanceof ApiError ? save.error.message : t("errorGeneric")}
          </Alert>
        )}

        {/* Language first: everything else is unreadable without it. */}
        <Card>
          <CardHeader title={t("settingsLanguage")} icon={<Languages className="h-5 w-5" />} />
          <CardBody>
            <OptionGrid columns={2}>
              {(Object.keys(LANGUAGE_LABELS) as Language[]).map((code) => (
                <OptionCard
                  key={code}
                  name="language"
                  value={code}
                  checked={language === code}
                  label={LANGUAGE_LABELS[code].native}
                  help={language === "en" ? LANGUAGE_LABELS[code].english : undefined}
                  onSelect={(value) => {
                    setLanguage(value as Language);
                    change("language", value as Language);
                  }}
                />
              ))}
            </OptionGrid>
          </CardBody>
        </Card>

        {groups.map((group) => (
          <Card key={group.key}>
            <CardHeader title={t(GROUP_LABELS[group.key])} icon={<Settings2 className="h-5 w-5" />} />
            <CardBody>
              <OptionGrid columns={isEasyMode ? 1 : 2}>
                {(options[group.key] ?? []).map((option) => (
                  <OptionCard
                    key={option.value}
                    name={group.key}
                    value={option.value}
                    checked={group.current === option.value}
                    label={s(option.label)}
                    help={option.help ? s(option.help) : undefined}
                    onSelect={group.onSelect}
                  />
                ))}
              </OptionGrid>
            </CardBody>
          </Card>
        ))}

        <Card>
          <CardBody className="flex items-start justify-between gap-4">
            <div>
              <label htmlFor="audio-guidance" className="block text-base font-semibold text-ink">
                {t("audioGuidanceLabel")}
              </label>
              <p className="mt-1 text-sm text-ink-muted">{t("audioGuidanceHelp")}</p>
            </div>
            <SwitchPrimitive.Root
              id="audio-guidance"
              checked={preferences.audio_guidance}
              onCheckedChange={(checked) => change("audio_guidance", checked)}
              className={cn(
                "relative h-8 w-14 shrink-0 rounded-full border-2 transition-colors",
                preferences.audio_guidance
                  ? "border-primary bg-primary"
                  : "border-line bg-surface-muted",
              )}
            >
              <SwitchPrimitive.Thumb
                className={cn(
                  "block h-6 w-6 rounded-full bg-white shadow transition-transform",
                  preferences.audio_guidance ? "translate-x-6" : "translate-x-0.5",
                )}
              />
            </SwitchPrimitive.Root>
          </CardBody>
        </Card>

        <div className="rounded-2xl border-2 border-primary/25 bg-primary-soft p-4 sm:p-5">
          <p className="text-base text-primary-ink">{t("previewSample")}</p>
        </div>

        {/* Retaking the assessment is offered, never required. */}
        <Card>
          <CardHeader title={t("settingsRetake")} description={t("settingsRetakeHelp")} />
          <CardBody className="flex flex-wrap gap-2">
            <Button variant="secondary" asChild>
              <Link to="/onboarding/assessment">
                <RotateCcw className="h-5 w-5" aria-hidden="true" />
                {t("settingsRetake")}
              </Link>
            </Button>
            <Button variant="ghost" asChild>
              <Link to="/home">{t("encounterBackHome")}</Link>
            </Button>
          </CardBody>
        </Card>

        <p className="text-center text-xs text-ink-subtle">{t("neverLockedNote")}</p>
      </div>
    </AppShell>
  );
}
