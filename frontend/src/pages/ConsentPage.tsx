import { useMutation, useQuery } from "@tanstack/react-query";
import * as SwitchPrimitive from "@radix-ui/react-switch";
import { FileLock2, ShieldCheck, Volume2, VolumeX } from "lucide-react";
import { useMemo, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { useSpeech } from "@/hooks/useSpeech";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type { ConsentContent, ConsentPurpose, ConsentState } from "@/types/api";

export function ConsentPage() {
  const { t, s, language } = useI18n();
  const { advance, isAdvancing } = useAdvance();
  const speech = useSpeech();
  const [decisions, setDecisions] = useState<Record<string, boolean>>({});
  const [declined, setDeclined] = useState(false);

  const content = useQuery({
    queryKey: ["consent-content"],
    queryFn: () => api.get<ConsentContent>("/consents/content"),
    staleTime: Infinity,
  });

  const items = content.data?.items ?? [];

  // Required purposes start granted (the patient is agreeing by continuing);
  // optional ones start off, so nothing optional is opted-in by default.
  const effective = useMemo(() => {
    const state: Record<string, boolean> = {};
    for (const item of items) {
      state[item.purpose] = decisions[item.purpose] ?? item.required;
    }
    return state;
  }, [items, decisions]);

  const submit = useMutation({
    mutationFn: (granted: boolean) =>
      api.post<ConsentState>("/consents", {
        decisions: items.map((item) => ({
          purpose: item.purpose,
          granted: granted ? effective[item.purpose] : false,
        })),
        language,
      }),
    onSuccess: (state) => {
      if (state.has_required_consents) {
        void advance(state.next_route);
      } else {
        setDeclined(true);
      }
    },
  });

  const spokenSummary = useMemo(() => {
    if (!content.data) return "";
    return [
      s(content.data.summary.title),
      s(content.data.summary.body),
      ...items.map((item) => `${s(item.title)}. ${s(item.what)} ${s(item.why)}`),
    ].join(" ");
  }, [content.data, items, s]);

  if (content.isLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={4}
        title={content.data ? s(content.data.summary.title) : t("consentHeading")}
        description={content.data ? s(content.data.summary.body) : undefined}
        announce={spokenSummary}
        onNext={() => submit.mutate(true)}
        nextLabel={t("consentAcceptAll")}
        isBusy={submit.isPending || isAdvancing}
        secondaryAction={
          <Button
            variant="ghost"
            size="md"
            onClick={() => submit.mutate(false)}
            disabled={submit.isPending}
          >
            {t("consentDecline")}
          </Button>
        }
        footerNote={content.data ? s(content.data.summary.withdraw) : undefined}
        aside={
          <Card>
            <CardHeader title={t("profileConsents")} icon={<FileLock2 className="h-5 w-5" />} />
            <CardBody className="space-y-2">
              <p className="text-sm text-ink-muted">
                {content.data ? s(content.data.summary.withdraw) : ""}
              </p>
              <p className="text-xs text-ink-subtle">
                {t("prototypeNoticeTitle")} · v{content.data?.version}
              </p>
            </CardBody>
          </Card>
        }
      >
        {declined && <Alert tone="warning" title={t("consentDecline")}>{t("consentDeclinedNotice")}</Alert>}

        {submit.error && (
          <Alert tone="danger">
            {submit.error instanceof ApiError ? submit.error.message : t("errorGeneric")}
          </Alert>
        )}

        {speech.isSupported && (
          <Button
            variant="secondary"
            size="md"
            onClick={() => (speech.isSpeaking ? speech.stop() : speech.speak(spokenSummary))}
          >
            {speech.isSpeaking ? (
              <>
                <VolumeX className="h-5 w-5" aria-hidden="true" />
                {t("consentStopListening")}
              </>
            ) : (
              <>
                <Volume2 className="h-5 w-5" aria-hidden="true" />
                {t("consentListen")}
              </>
            )}
          </Button>
        )}

        <ul className="space-y-4">
          {items.map((item) => (
            <li
              key={item.purpose}
              className="rounded-2xl border-2 border-line bg-surface p-4 sm:p-5"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="text-lg font-semibold text-ink">{s(item.title)}</h2>
                    <Badge tone={item.required ? "info" : "neutral"}>
                      {item.required ? t("consentRequiredTag") : t("consentOptionalTag")}
                    </Badge>
                  </div>

                  <dl className="mt-3 space-y-2 text-base">
                    {(
                      [
                        ["consentWhatLabel", item.what],
                        ["consentWhyLabel", item.why],
                        ["consentHowLabel", item.how],
                      ] as const
                    ).map(([labelKey, value]) => (
                      <div key={labelKey}>
                        <dt className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">
                          {t(labelKey)}
                        </dt>
                        <dd className="text-ink-muted">{s(value)}</dd>
                      </div>
                    ))}
                  </dl>
                </div>

                {/* Required purposes are not switchable: declining them means
                    declining the whole step, which the footer action handles. */}
                {item.required ? (
                  <ShieldCheck className="h-6 w-6 shrink-0 text-success" aria-hidden="true" />
                ) : (
                  <SwitchPrimitive.Root
                    checked={effective[item.purpose] ?? false}
                    onCheckedChange={(checked) =>
                      setDecisions((current) => ({
                        ...current,
                        [item.purpose as ConsentPurpose]: checked,
                      }))
                    }
                    aria-label={s(item.title)}
                    className={cn(
                      "relative h-8 w-14 shrink-0 rounded-full border-2 transition-colors",
                      effective[item.purpose]
                        ? "border-primary bg-primary"
                        : "border-line bg-surface-muted",
                    )}
                  >
                    <SwitchPrimitive.Thumb
                      className={cn(
                        "block h-6 w-6 rounded-full bg-white shadow transition-transform",
                        effective[item.purpose] ? "translate-x-6" : "translate-x-0.5",
                      )}
                    />
                  </SwitchPrimitive.Root>
                )}
              </div>
            </li>
          ))}
        </ul>
      </StepLayout>
    </AppShell>
  );
}
