import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, BadgeInfo, CheckCircle2, Sparkles, Volume2, VolumeX } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardFooter } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/Progress";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { useSpeech } from "@/hooks/useSpeech";
import { AnswerInput, type AnswerDraft } from "@/features/interview/AnswerInput";
import type { AiStatus, InterviewView } from "@/types/api";

/**
 * The interview screen: exactly one meaningful question at a time.
 *
 * The server decides what is asked and when the interview is finished; this
 * page only renders the current question and posts the answer.
 */
export function InterviewPage() {
  const { t } = useI18n();
  const { isEasyMode, preferences, isLoading: preferencesLoading } = usePreferences();
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const speech = useSpeech();
  const [includeAyush, setIncludeAyush] = useState(false);

  const aiStatus = useQuery({
    queryKey: ["ai-status"],
    queryFn: () => api.get<AiStatus>("/interview/ai-status"),
    staleTime: 60_000,
  });

  const session = useQuery({
    queryKey: ["interview"],
    queryFn: () => api.post<InterviewView>("/interview/start", { include_ayush: includeAyush }),
  });

  const view = session.data;

  const answer = useMutation({
    mutationFn: (draft: AnswerDraft) =>
      api.post<InterviewView>(`/interview/${view!.session_id}/answer`, {
        instance_key: view!.question!.instance_key,
        text: draft.text,
        input_method: draft.method,
      }),
    onSuccess: (next) => {
      queryClient.setQueryData(["interview"], next);
      // The profile and timeline both change as answers land.
      void queryClient.invalidateQueries({ queryKey: ["medical-profile"] });
    },
  });

  const back = useMutation({
    mutationFn: () => api.post<InterviewView>(`/interview/${view!.session_id}/back`),
    onSuccess: (next) => queryClient.setQueryData(["interview"], next),
  });

  const question = view?.question ?? null;

  // Read the question aloud when the patient asked for audio guidance.
  useEffect(() => {
    if (!question || !preferences.audio_guidance) return;
    speech.announce(`${question.text}. ${question.help}`);
    return speech.stop;
    // eslint-disable-next-line react-hooks/exhaustive-deps -- announce per question
  }, [question?.instance_key, preferences.audio_guidance]);

  if (session.isLoading || preferencesLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (session.isError || !view) {
    return (
      <AppShell>
        <ErrorPanel
          message={session.error instanceof ApiError ? session.error.message : t("errorNetwork")}
          onRetry={() => void session.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  // --- finished ---------------------------------------------------------
  if (view.complete || !question) {
    return (
      <AppShell>
        <Card>
          <CardBody className="space-y-6 py-9 text-center">
            <span
              aria-hidden="true"
              className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-success-soft text-success"
            >
              <CheckCircle2 className="h-11 w-11" />
            </span>
            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-ink">{t("interviewDone")}</h1>
              <p className="mx-auto max-w-xl text-lg text-ink-muted">{t("interviewDoneBody")}</p>
            </div>
            <ProgressBar percent={100} label={`${view.progress.answered} ${t("medicalItemsAdded")}`} />
            <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
              <Button size="lg" asChild>
                <Link to="/records">{t("recordsHeading")}</Link>
              </Button>
              <Button size="lg" variant="secondary" asChild>
                <Link to="/review">{t("reviewHeading")}</Link>
              </Button>
            </div>
          </CardBody>
        </Card>
      </AppShell>
    );
  }

  const spoken = `${question.text}. ${question.help}`;

  return (
    <AppShell>
      <div className="space-y-4">
        {/* Progress: section position, not just a bar. */}
        <div className="space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm font-semibold text-ink-muted">
              {t("sectionOf")} {view.progress.section_index + 1} {t("assessmentOf")}{" "}
              {view.progress.section_count} · {question.section_title}
            </p>
            <p className="text-sm text-ink-subtle">{view.progress.percent}%</p>
          </div>
          <ProgressBar percent={view.progress.percent} />
        </div>

        {/* Honest when AI assistance is down — and that nothing was lost. */}
        {view.ai_fallback_active && (
          <Alert tone="warning" title={t("interviewAiFallback")} />
        )}

        {view.retry_hint && <Alert tone="warning">{view.retry_hint}</Alert>}

        <Card>
          <CardBody className={cn("space-y-5", isEasyMode && "py-7")}>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 space-y-2">
                <div className="flex flex-wrap items-center gap-2">
                  {question.about && (
                    <Badge tone="info">
                      {t("interviewAboutThis")} {question.about}
                    </Badge>
                  )}
                  {question.is_ai_suggested && (
                    <Badge tone="neutral" icon={<Sparkles className="h-3.5 w-3.5" />}>
                      {t("interviewAiSuggested")}
                    </Badge>
                  )}
                </div>
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

        {/* AYUSH opt-in, offered without forcing anyone through it. */}
        {view.progress.section_count === 9 && !isEasyMode && (
          <Card>
            <CardBody className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-start gap-3">
                <BadgeInfo className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                <div>
                  <p className="font-semibold text-ink">{t("interviewAyushOffer")}</p>
                  <p className="text-sm text-ink-muted">{t("interviewAyushHelp")}</p>
                </div>
              </div>
              <Button
                variant="secondary"
                onClick={() => {
                  setIncludeAyush(true);
                  navigate("/ayush");
                }}
              >
                {t("ayushInclude")}
              </Button>
            </CardBody>
          </Card>
        )}

        {aiStatus.data && !aiStatus.data.available && !view.ai_fallback_active && (
          <p className="text-center text-xs text-ink-subtle">{t("interviewAiFallback")}</p>
        )}
      </div>
    </AppShell>
  );
}
