import { useMutation, useQuery } from "@tanstack/react-query";
import { CheckCircle2, FileText, Sparkles, UserRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { sourceSentence } from "@/lib/enumLabels";
import type { HistoryEntry, InterviewView, StructuredHistory } from "@/types/api";

/**
 * The review screen: structured sections, not a wall of text, with patient
 * statements and document findings kept visibly separate.
 */
export function ReviewPage() {
  const { t, s, language } = useI18n();
  const navigate = useNavigate();

  const history = useQuery({
    queryKey: ["structured-history"],
    queryFn: () => api.get<StructuredHistory>("/patients/me/medical-profile/structured"),
  });

  const session = useQuery({
    queryKey: ["interview-current"],
    queryFn: () => api.get<InterviewView | null>("/interview/current"),
  });

  const confirm = useMutation({
    mutationFn: () =>
      api.post<InterviewView>(`/interview/${session.data!.session_id}/confirm`),
    onSuccess: () => navigate("/profile"),
  });

  if (history.isLoading) {
    return (
      <AppShell wide>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (history.isError || !history.data) {
    return (
      <AppShell wide>
        <ErrorPanel
          message={history.error instanceof ApiError ? history.error.message : t("errorNetwork")}
          onRetry={() => void history.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const data = history.data;
  const populated = Object.entries(data.sections).filter(([, entries]) => entries.length > 0);

  const renderEntry = (entry: HistoryEntry, index: number) => {
    const fromDocument = entry.source === "document";
    const detail = [entry.attributes.dose, entry.attributes.frequency, entry.attributes.duration]
      .filter(Boolean)
      .join(" · ");
    return (
      <li
        key={`${entry.value}-${index}`}
        className="flex flex-wrap items-start justify-between gap-2 rounded-xl border border-line bg-surface-muted px-4 py-3"
      >
        <div className="min-w-0">
          <p className="text-base font-medium text-ink">{entry.value}</p>
          {detail && <p className="text-sm text-ink-muted">{detail}</p>}
          {entry.note && (
            <p className="text-sm text-ink-subtle">
              {sourceSentence(entry.note, entry.note_source, language)}
            </p>
          )}
        </div>
        <Badge tone={fromDocument ? "info" : "neutral"}>
          {fromDocument ? t("reviewSourceDocument") : t("reviewSourcePatient")}
        </Badge>
      </li>
    );
  };

  return (
    <AppShell wide backRoute="/home" backLabel={t("backToHome")}>
      <div className="space-y-5">
        <div>
          <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("reviewHeading")}</h1>
          <p className="mt-1 text-base text-ink-muted">{t("reviewBody")}</p>
        </div>

        <Alert tone="info">{s(data.disclaimer)}</Alert>

        <div className="flex flex-wrap gap-3">
          <Badge tone="neutral" icon={<UserRound className="h-3.5 w-3.5" />}>
            {t("reviewYouTold")}: {data.patient_reported_count}
          </Badge>
          <Badge tone="info" icon={<FileText className="h-3.5 w-3.5" />}>
            {t("reviewFromDocuments")}: {data.document_derived_count}
          </Badge>
          {data.ayush_included && <Badge tone="success">{t("ayushHeading")}</Badge>}
        </div>

        {/* Missing information is surfaced, never hidden. */}
        {data.missing_sections.length > 0 && (
          <Card className="border-warning/35 bg-warning-soft">
            <CardHeader title={t("reviewMissing")} description={t("reviewMissingBody")} />
            <CardBody className="space-y-3">
              <div className="flex flex-wrap gap-2">
                {data.missing_sections.map((key) => (
                  <Badge key={key} tone="warning">
                    {data.labels[key] ?? key}
                  </Badge>
                ))}
              </div>
              <Button variant="secondary" asChild>
                <Link to="/interview">{t("interviewResume")}</Link>
              </Button>
            </CardBody>
          </Card>
        )}

        <Card>
          <CardHeader
            title={t("reviewSummary")}
            icon={<Sparkles className="h-5 w-5" />}
            action={
              <Badge tone="neutral">
                {data.narrative_source === "ai" ? "AI" : t("appName")}
              </Badge>
            }
          />
          <CardBody>
            <p className="whitespace-pre-line text-base leading-relaxed text-ink">
              {data.narrative}
            </p>
          </CardBody>
        </Card>

        {/* Progressive disclosure: one card per section, only if it has content. */}
        <div className="grid gap-4 lg:grid-cols-2">
          {populated.map(([key, entries]) => (
            <Card key={key}>
              <CardHeader
                title={data.labels[key] ?? key}
                action={
                  <Button variant="ghost" size="md" asChild>
                    <Link to="/onboarding/medical-profile">{t("reviewEditSection")}</Link>
                  </Button>
                }
              />
              <CardBody>
                <ul className="space-y-2">{entries.map(renderEntry)}</ul>
              </CardBody>
            </Card>
          ))}
        </div>

        {populated.length === 0 && (
          <Alert tone="warning" title={t("reviewNothingRecorded")}>
            <Button variant="secondary" asChild className="mt-2">
              <Link to="/interview">{t("interviewStart")}</Link>
            </Button>
          </Alert>
        )}

        <Card>
          <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-base text-ink-muted">{t("reviewBody")}</p>
            <div className="flex flex-wrap gap-2">
              <Button variant="secondary" asChild>
                <Link to="/timeline">{t("timelineHeading")}</Link>
              </Button>
              {session.data ? (
                <Button
                  size="lg"
                  disabled={confirm.isPending}
                  onClick={() => confirm.mutate()}
                >
                  <CheckCircle2 className="h-5 w-5" aria-hidden="true" />
                  {confirm.isPending ? t("saving") : t("reviewConfirm")}
                </Button>
              ) : (
                <Button size="lg" asChild>
                  <Link to="/home">{t("encounterBackHome")}</Link>
                </Button>
              )}
            </div>
          </CardBody>
        </Card>

        {confirm.error && (
          <Alert tone="danger">
            {confirm.error instanceof ApiError ? confirm.error.message : t("errorGeneric")}
          </Alert>
        )}
      </div>
    </AppShell>
  );
}
