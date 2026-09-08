import { useMutation, useQuery } from "@tanstack/react-query";
import * as SwitchPrimitive from "@radix-ui/react-switch";
import { Lightbulb, SlidersHorizontal, Sparkles } from "lucide-react";
import { useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type {
  AssessmentContent,
  ContrastMode,
  FontSize,
  InteractionPreference,
  InterfaceMode,
  Preferences,
  PreferencesPayload,
  Recommendation,
} from "@/types/api";

const GROUP_LABELS = {
  interface_mode: "interfaceModeLabel",
  font_size: "fontSizeLabel",
  contrast_mode: "contrastLabel",
  interaction_preference: "interactionLabel",
} as const;

export function PreferencesPage() {
  const { t, s, language } = useI18n();
  const { preferences, preview, invalidate, isEasyMode } = usePreferences();
  const { advance, isAdvancing } = useAdvance();
  const [customising, setCustomising] = useState(false);
  const [draft, setDraft] = useState<Partial<Preferences>>({});

  const recommendation = useQuery({
    queryKey: ["recommendation"],
    queryFn: () => api.get<Recommendation | null>("/accessibility/recommendation"),
  });

  const content = useQuery({
    queryKey: ["assessment-content"],
    queryFn: () => api.get<AssessmentContent>("/accessibility/content"),
    staleTime: Infinity,
  });

  const confirm = useMutation({
    mutationFn: (accepted: boolean) => {
      const payload: PreferencesPayload = accepted
        ? { accepted_recommendation: true }
        : { ...draft, accepted_recommendation: false };
      return api.put<Preferences>("/accessibility/preferences", payload);
    },
    onSuccess: () => {
      invalidate();
      void advance("/onboarding/consent");
    },
  });

  /** Change a setting and apply it immediately, so the effect is visible. */
  const change = <K extends keyof Preferences>(key: K, value: Preferences[K]) => {
    setDraft((current) => ({ ...current, [key]: value }));
    preview({ [key]: value } as Partial<Preferences>);
  };

  if (recommendation.isLoading || content.isLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  const reasons = recommendation.data?.reasons ?? [];
  const options = content.data?.preference_options ?? {};

  const groups: Array<{
    key: keyof typeof GROUP_LABELS;
    current: string;
    onSelect: (value: string) => void;
  }> = [
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
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={3}
        title={t("recommendationHeading")}
        description={t("recommendationBody")}
        onNext={() => confirm.mutate(!customising)}
        nextLabel={customising ? t("save") : t("recommendationAccept")}
        isBusy={confirm.isPending || isAdvancing}
        secondaryAction={
          !customising ? (
            <Button variant="secondary" size="md" onClick={() => setCustomising(true)}>
              <SlidersHorizontal className="h-5 w-5" aria-hidden="true" />
              {t("recommendationCustomise")}
            </Button>
          ) : undefined
        }
        footerNote={t("neverLockedNote")}
        aside={
          reasons.length > 0 ? (
            <Card>
              <CardHeader title={t("assessmentWhyTitle")} icon={<Lightbulb className="h-5 w-5" />} />
              <CardBody>
                <ul className="space-y-3">
                  {reasons.map((reason) => (
                    <li key={reason.code} className="flex gap-2 text-sm text-ink-muted">
                      <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                      {language === "hi" ? reason.hi : reason.en}
                    </li>
                  ))}
                </ul>
              </CardBody>
            </Card>
          ) : undefined
        }
      >
        {confirm.error && (
          <Alert tone="danger">
            {confirm.error instanceof ApiError ? confirm.error.message : t("errorGeneric")}
          </Alert>
        )}

        {/* Why, in the patient's own terms — visible in Easy Mode too. */}
        {isEasyMode && reasons.length > 0 && (
          <Alert tone="info" title={t("assessmentWhyTitle")}>
            <ul className="space-y-2">
              {reasons.map((reason) => (
                <li key={reason.code}>{language === "hi" ? reason.hi : reason.en}</li>
              ))}
            </ul>
          </Alert>
        )}

        {/* Live preview: the settings are already applied to this screen. */}
        <div className="rounded-2xl border-2 border-primary/25 bg-primary-soft/50 p-4 sm:p-5">
          <p className="text-sm font-semibold uppercase tracking-wide text-primary-ink">
            {t("previewLabel")}
          </p>
          <p className="mt-2 text-ink">{t("previewSample")}</p>
        </div>

        {customising ? (
          <div className="space-y-7">
            {groups.map((group) => (
              <fieldset key={group.key} className="space-y-3">
                <legend className="block text-base font-semibold text-ink">
                  {t(GROUP_LABELS[group.key])}
                </legend>
                <OptionGrid columns={isEasyMode ? 1 : 2}>
                  {(options[group.key] ?? []).map((option) => (
                    <OptionCard
                      key={option.value}
                      name={group.key}
                      value={option.value}
                      checked={group.current === option.value}
                      onSelect={group.onSelect}
                      label={s(option.label)}
                      help={option.help ? s(option.help) : undefined}
                    />
                  ))}
                </OptionGrid>
              </fieldset>
            ))}

            {/* Audio guidance is a switch, not a card set. */}
            <div className="flex items-start justify-between gap-4 rounded-2xl border-2 border-line bg-surface p-4 sm:p-5">
              <div>
                <label
                  htmlFor="audio-guidance"
                  className="block text-base font-semibold text-ink"
                >
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
            </div>
          </div>
        ) : (
          <dl className="grid gap-3 sm:grid-cols-2">
            {groups.map((group) => {
              const match = (options[group.key] ?? []).find(
                (option) => option.value === group.current,
              );
              return (
                <div
                  key={group.key}
                  className="rounded-xl border border-line bg-surface-muted px-4 py-3"
                >
                  <dt className="text-sm font-medium text-ink-muted">
                    {t(GROUP_LABELS[group.key])}
                  </dt>
                  <dd className="mt-0.5 text-lg font-semibold text-ink">
                    {match ? s(match.label) : group.current}
                  </dd>
                </div>
              );
            })}
            <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
              <dt className="text-sm font-medium text-ink-muted">{t("audioGuidanceLabel")}</dt>
              <dd className="mt-0.5 text-lg font-semibold text-ink">
                {preferences.audio_guidance ? t("yes") : t("no")}
              </dd>
            </div>
          </dl>
        )}
      </StepLayout>
    </AppShell>
  );
}
