import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, CheckCircle2, Info, Sparkles, Volume2, VolumeX } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardFooter, CardHeader } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/Progress";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { useSpeech } from "@/hooks/useSpeech";
import { AnswerInput, type AnswerDraft } from "@/features/interview/AnswerInput";
import { SafetyScreen, UrgentBanner } from "@/features/encounter/SafetyScreen";
import type { EncounterView, ExistingContext } from "@/types/api";

/**
 * The new-visit interview.
 *
 * Two things distinguish it from the Phase 2 profile interview:
 *
 * 1. It asks about today only. The patient's history arrives as read-only
 *    context (`existing`) and is shown as "we already know about…".
 * 2. Every answer is re-screened for red flags server-side. When one is
 *    raised, the emergency screen interrupts — and continuing from it does
 *    not clear the flag.
 */
export function VisitPage() {
  const { t } = useI18n();
  const { isEasyMode, preferences, isLoading: preferencesLoading } = usePreferences();
  const queryClient = useQueryClient();
  const speech = useSpeech();

  // Set once the patient has dismissed the emergency screen this session.
  const [safetySeen, setSafetySeen] = useState(false);
  const [assistanceSent, setAssistanceSent] = useState(false);

  const visit = useQuery({
    queryKey: ["visit"],
    queryFn: () => api.post<EncounterView>("/encounters/start", {}),
  });

  const view = visit.data;
  const encounterId = view?.encounter_id;

  const answer = useMutation({
    mutationFn: (draft: AnswerDraft) =>
      api.post<EncounterView>(`/encounters/${encounterId}/answer`, {
        instance_key: view!.question!.instance_key,
        text: draft.text,
        input_method: draft.method,
      }),
    onSuccess: (next) => {
      queryClient.setQueryData(["visit"], next);
      void queryClient.invalidateQueries({ queryKey: ["home"] });
    },
  });

  const back = useMutation({
    mutationFn: () => api.post<EncounterView>(`/encounters/${encounterId}/back`),
    onSuccess: (next) => queryClient.setQueryData(["visit"], next),
  });

  const acknowledge = useMutation({
    mutationFn: () =>
      api.post<EncounterView>(`/encounters/${encounterId}/safety/acknowledge`),
    onSuccess: (next) => {
      queryClient.setQueryData(["visit"], next);
      setSafetySeen(true);
    },
  });

  const assistance = useMutation({
    mutationFn: () =>
      api.post<EncounterView>(`/encounters/${encounterId}/safety/assistance`),
    onSuccess: (next) => {
      queryClient.setQueryData(["visit"], next);
      setAssistanceSent(true);
    },
  });

  const question = view?.question ?? null;

  useEffect(() => {
    if (!question || !preferences.audio_guidance) return;
    speech.announce(`${question.text}. ${question.help}`);
    return speech.stop;
    // eslint-disable-next-line react-hooks/exhaustive-deps -- announce per question
  }, [question?.instance_key, preferences.audio_guidance]);

  if (visit.isLoading || preferencesLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (visit.isError || !view) {
    return (
      <AppShell>
        <ErrorPanel
          message={visit.error instanceof ApiError ? visit.error.message : t("errorNetwork")}
          onRetry={() => void visit.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const isUrgent = view.safety.status === "active";

  // --- emergency interrupt ---------------------------------------------
  // Shown as soon as a flag is raised, before anything else on the screen.
  if (isUrgent && !view.safety.acknowledged && !safetySeen) {
    return (
      <AppShell>
        <SafetyScreen
          safety={view.safety}
          isBusy={acknowledge.isPending || assistance.isPending}
          assistanceSent={assistanceSent}
          onRequestAssistance={() => assistance.mutate()}
          onContinue={() => acknowledge.mutate()}
        />
      </AppShell>
    );
  }

  // --- finished ---------------------------------------------------------
  if (view.complete || !question) {
    return (
      <AppShell>
        <div className="space-y-4">
          {isUrgent && <UrgentBanner />}
          <Card>
            <CardBody className="space-y-6 py-9 text-center">
              <span
                aria-hidden="true"
                className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-success-soft text-success"
              >
                <CheckCircle2 className="h-11 w-11" />
              </span>
              <div className="space-y-2">
                <h1 className="text-3xl font-bold text-ink">{t("visitDone")}</h1>
                <p className="mx-auto max-w-xl text-lg text-ink-muted">{t("visitDoneBody")}</p>
              </div>
              <Button size="xl" asChild className="mx-auto w-full max-w-form">
                <Link to={`/visit/${view.encounter_id}/review`}>{t("visitReview")}</Link>
              </Button>
            </CardBody>
          </Card>
        </div>
      </AppShell>
    );
  }

  const spoken = `${question.text}. ${question.help}`;

  return (
    <AppShell>
      <div className="space-y-4">
        {isUrgent && <UrgentBanner />}

        <div className="space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm font-semibold text-ink-muted">
              {question.section_title} · {t("visitTodayOnly")}
            </p>
            <p className="text-sm text-ink-subtle">{view.progress.percent}%</p>
          </div>
          <ProgressBar percent={view.progress.percent} />
        </div>

        {view.ai_fallback_active && <Alert tone="warning" title={t("interviewAiFallback")} />}
        {view.retry_hint && <Alert tone="warning">{view.retry_hint}</Alert>}

        <Card>
          <CardBody className={cn("space-y-5", isEasyMode && "py-7")}>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 space-y-2">
                {question.is_ai_suggested && (
                  <Badge tone="neutral" icon={<Sparkles className="h-3.5 w-3.5" />}>
                    {t("interviewAiSuggested")}
                  </Badge>
                )}
                <h1
                  className={cn(
                    "font-bold leading-snug text-ink",
                    isEasyMode ? "text-3xl" : "text-2xl",
                  )}
                >
                  {question.text}
                </h1>
                {question.help && (
                  <p className={cn("text-ink-muted", isEasyMode ? "text-lg" : "text-base")}>
                    {question.help}
                  </p>
                )}
              </div>
              {speech.isSupported && speech.hasVoiceForLanguage && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => (speech.isSpeaking ? speech.stop() : speech.speak(spoken))}
                  aria-label={speech.isSpeaking ? t("consentStopListening") : t("consentListen")}
                >
                  {speech.isSpeaking ? (
                    <VolumeX className="h-5 w-5" aria-hidden="true" />
                  ) : (
                    <Volume2 className="h-5 w-5" aria-hidden="true" />
                  )}
                </Button>
              )}
            </div>

            {answer.error && (
              <Alert tone="danger">
                {answer.error instanceof ApiError ? answer.error.message : t("errorGeneric")}
              </Alert>
            )}

            <AnswerInput
              question={question}
              disabled={answer.isPending || back.isPending}
              onSubmit={(draft) => answer.mutate(draft)}
            />
          </CardBody>

          <CardFooter>
            <Button
              variant="ghost"
              onClick={() => back.mutate()}
              disabled={back.isPending || view.progress.answered === 0}
            >
              <ArrowLeft className="h-5 w-5" aria-hidden="true" />
              {t("back")}
            </Button>
            <p className="text-sm text-ink-subtle">{t("progressSavedNote")}</p>
          </CardFooter>
        </Card>

        {/* What we already know — shown so the patient sees why we are not
            asking for it again. Read-only here by design. */}
        {!isEasyMode && <ExistingKnowledge existing={view.existing} />}
      </div>
    </AppShell>
  );
}

export function ExistingKnowledge({ existing }: { existing: ExistingContext }) {
  const { t } = useI18n();
  const groups: Array<[string, string[]]> = [
    [t("homeConditions"), existing.conditions],
    [t("homeMedications"), existing.medications],
    [t("homeAllergies"), existing.allergies],
  ];
  if (groups.every(([, values]) => values.length === 0)) return null;

  return (
    <Card>
      <CardHeader
        title={t("visitWeKnow")}
        description={t("visitWeKnowHelp")}
        icon={<Info className="h-5 w-5" />}
        action={
          <Button variant="ghost" size="md" asChild>
            <Link to="/onboarding/medical-profile">{t("edit")}</Link>
          </Button>
        }
      />
      <CardBody>
        <dl className="grid gap-3 sm:grid-cols-3">
          {groups.map(([label, values]) =>
            values.length === 0 ? null : (
              <div key={label}>
                <dt className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">
                  {label}
                </dt>
                <dd className="mt-1 flex flex-wrap gap-1.5">
                  {values.map((value) => (
                    <span
                      key={value}
                      className="rounded-full border border-line bg-surface-muted px-2.5 py-1 text-sm text-ink"
                    >
                      {value}
                    </span>
                  ))}
                </dd>
              </div>
            ),
          )}
        </dl>
      </CardBody>
    </Card>
  );
}
