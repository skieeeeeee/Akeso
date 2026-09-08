import { useMutation, useQuery } from "@tanstack/react-query";
import * as CheckboxLike from "@radix-ui/react-switch";
import {
  BookOpen,
  CheckCircle2,
  ClipboardList,
  FileText,
  History,
  Sparkles,
  UserRound,
} from "lucide-react";
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { HandoffCode } from "@/features/encounter/HandoffCode";
import { UrgentBanner } from "@/features/encounter/SafetyScreen";
import { ExistingKnowledge } from "./VisitPage";
import type { EncounterReview, EncounterSubmission } from "@/types/api";
import type { StringKey } from "@/lib/strings";

// The examination groups, in the order they were asked.
const AYUSH_GROUPS: [string, StringKey][] = [
  ["dashavidha", "ayushDashavidha"],
  ["ashtasthana", "ayushAshtasthana"],
  ["lifestyle", "ayushLifestyle"],
  ["ahara", "ayushAhara"],
  ["vihara", "ayushVihara"],
];

type Confirmation = {
  symptoms_correct: boolean;
  reviewed_information: boolean;
  understands_use: boolean;
};

/**
 * The pre-submission review.
 *
 * Today's answers are editable (by going back into the visit); existing
 * history is displayed read-only, so a patient correcting today's symptoms
 * cannot accidentally rewrite their medical record.
 */
export function VisitReviewPage() {
  const { t, s, v } = useI18n();
  const { isEasyMode } = usePreferences();
  const { encounterId = "" } = useParams();
  const navigate = useNavigate();

  const [confirmation, setConfirmation] = useState<Confirmation>({
    symptoms_correct: false,
    reviewed_information: false,
    understands_use: false,
  });
  const [submitted, setSubmitted] = useState<EncounterSubmission | null>(null);

  const review = useQuery({
    queryKey: ["visit-review", encounterId],
    queryFn: () => api.get<EncounterReview>(`/encounters/${encounterId}/review`),
    enabled: Boolean(encounterId),
  });

  const submit = useMutation({
    mutationFn: () =>
      api.post<EncounterSubmission>(`/encounters/${encounterId}/submit`, confirmation),
    onSuccess: setSubmitted,
  });

  if (review.isLoading) {
    return (
      <AppShell wide>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (review.isError || !review.data) {
    return (
      <AppShell wide>
        <ErrorPanel
          message={review.error instanceof ApiError ? review.error.message : t("errorNetwork")}
          onRetry={() => void review.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const data = review.data;
  const isUrgent = data.safety.status === "active";
  const allConfirmed =
    confirmation.symptoms_correct &&
    confirmation.reviewed_information &&
    confirmation.understands_use;

  // --- submitted --------------------------------------------------------
  if (submitted || data.submitted_at) {
    const message = submitted?.message;
    return (
      <AppShell wide>
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
                <h1 className="text-3xl font-bold text-ink">{t("handoffHeading")}</h1>
                <p className="mx-auto max-w-xl text-lg text-ink-muted">{t("handoffBody")}</p>
              </div>

              {/* The visit itself, in a code. This used to say the visit had
                  been "sent" and ask the patient to wait — but nothing was
                  delivered anywhere a clinician could see, so they were
                  waiting for something that was never going to arrive. */}
              {encounterId && <HandoffCode encounterId={encounterId} />}

              <p className="mx-auto max-w-xl text-sm text-ink-subtle">
                {t("handoffPrivacy")}
              </p>

              <div className="mx-auto w-full max-w-form space-y-2">
                <Button variant="secondary" size="lg" block asChild>
                  <Link to="/home">{t("encounterBackHome")}</Link>
                </Button>
                <p className="text-sm text-ink-subtle">
                  {message ? s(message) : t("encounterAlreadySubmitted")}
                </p>
              </div>
            </CardBody>
          </Card>
        </div>
      </AppShell>
    );
  }

  const confirmRow = (
    key: keyof Confirmation,
    label: string,
  ) => (
    <div
      key={key}
      className="flex items-start justify-between gap-4 rounded-xl border border-line bg-surface-muted px-4 py-3"
    >
      <label htmlFor={key} className="text-base text-ink">
        {label}
      </label>
      <CheckboxLike.Root
        id={key}
        checked={confirmation[key]}
        onCheckedChange={(checked) =>
          setConfirmation((current) => ({ ...current, [key]: checked }))
        }
        className={cn(
          "relative h-8 w-14 shrink-0 rounded-full border-2 transition-colors",
          confirmation[key] ? "border-primary bg-primary" : "border-line bg-surface",
        )}
      >
        <CheckboxLike.Thumb
          className={cn(
            "block h-6 w-6 rounded-full bg-white shadow transition-transform",
            confirmation[key] ? "translate-x-6" : "translate-x-0.5",
          )}
        />
      </CheckboxLike.Root>
    </div>
  );

  return (
    <AppShell wide>
      <div className="space-y-5">
        {isUrgent && <UrgentBanner />}

        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-ink sm:text-3xl">
              {t("encounterReviewHeading")}
            </h1>
            <p className="mt-1 text-base text-ink-muted">{t("encounterReviewBody")}</p>
          </div>
        </div>

        <Alert tone="info">{s(data.disclaimer)}</Alert>

        {data.missing.length > 0 && (
          <Alert tone="warning" title={t("encounterMissing")}>
            <div className="mt-1 flex flex-wrap gap-2">
              {data.missing.map((key) => (
                <Badge key={key} tone="warning">
                  {data.labels[key] ?? key}
                </Badge>
              ))}
            </div>
            <Button variant="secondary" size="md" asChild className="mt-3">
              <Link to="/visit">{t("encounterEditToday")}</Link>
            </Button>
          </Alert>
        )}

        {/* Today's concern */}
        <Card>
          <CardHeader
            title={t("encounterTodayConcern")}
            icon={<ClipboardList className="h-5 w-5" />}
            action={
              <Button variant="ghost" size="md" asChild>
                <Link to="/visit">{t("encounterEditToday")}</Link>
              </Button>
            }
          />
          <CardBody>
            <p className={isEasyMode ? "text-2xl font-semibold text-ink" : "text-xl font-semibold text-ink"}>
              {data.chief_complaint ?? t("homeNothingYet")}
            </p>
          </CardBody>
        </Card>

        {/* Severity as a labelled metric — not another answer row. */}
        {data.severity && (
          <Card>
            <CardBody className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-sm text-ink-muted">{t("encounterSeverity")}</p>
                <p className="mt-0.5 text-3xl font-bold tabular-nums text-ink">
                  {data.severity.split("/")[0]}
                  <span className="ml-2 text-base font-normal text-ink-muted">
                    {t("encounterSeverityScale")}
                  </span>
                </p>
              </div>
              {/* Explains why a low rating can still be urgent. */}
              {isUrgent && (
                <p className="max-w-xs text-sm text-danger-ink">{t("encounterUrgentReason")}</p>
              )}
            </CardBody>
          </Card>
        )}

        {/* What the patient told us today — one view, grouped by section. */}
        <Card>
          <CardHeader title={t("encounterFollowUps")} icon={<UserRound className="h-5 w-5" />} />
          <CardBody className="space-y-4">
            {data.today_answers.length > 0 ? (
              <ul className="space-y-2">
                {data.today_answers.map((entry, index) => (
                  <li
                    key={`${entry.question_text}-${index}`}
                    className="rounded-xl border border-line bg-surface-muted px-4 py-3"
                  >
                    <p className="text-sm text-ink-subtle">{entry.question_text}</p>
                    <p className="text-base font-medium text-ink">{entry.answer}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-base text-ink-muted">{t("homeNothingYet")}</p>
            )}

            {/* Skipped questions are counted, never listed as answers. */}
            {data.skipped_count > 0 && (
              <p className="text-sm text-ink-subtle">
                {data.skipped_count} {t("encounterSkipped")}
              </p>
            )}
          </CardBody>
        </Card>

        {/* An Ayurvedic visit asks around twenty more questions, and those
            answers go to the assessment rather than the medical profile. They
            are shown here so a patient who answered thirty-three questions
            does not reach this screen and see five. */}
        {data.ayush && data.ayush.entries.length > 0 && (
          <Card>
            <CardHeader
              title={t("ayushRecordedHeading")}
              icon={<BookOpen className="h-5 w-5" />}
              action={
                <span className="text-sm text-ink-muted">
                  {t("ayushRecordedCount")
                    .replace("{count}", String(data.ayush.count))
                    .replace("{total}", String(data.ayush.total))}
                </span>
              }
            />
            <CardBody className="space-y-4">
              {AYUSH_GROUPS.map(([group, heading]) => {
                const rows = data.ayush!.entries.filter((row) => row.group === group);
                if (rows.length === 0) return null;
                // Diet and routine are multi-select, so they read as chips
                // rather than as question-and-answer rows.
                const isList = group === "ahara" || group === "vihara";
                return (
                  <div key={group}>
                    <p className="mb-2 text-sm font-semibold text-ink-muted">{t(heading)}</p>
                    {isList ? (
                      <ul className="flex flex-wrap gap-2">
                        {rows.map((row, index) => (
                          <li key={`${group}-${index}`}>
                            <Badge tone="neutral">{row.answer}</Badge>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <ul className="space-y-2">
                        {rows.map((row, index) => (
                          <li
                            key={`${group}-${index}`}
                            className="rounded-xl border border-line bg-surface-muted px-4 py-3"
                          >
                            <p className="text-sm text-ink-subtle">
                              {row.question}
                              {row.term && (
                                <span className="ml-2 text-ink-subtle/80">· {row.term}</span>
                              )}
                            </p>
                            <p className="text-base font-medium text-ink">{row.answer}</p>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              })}
              <p className="text-sm text-ink-subtle">{t("ayushNotDiagnostic")}</p>
            </CardBody>
          </Card>
        )}

        {/* Existing history — read-only here, by design. */}
        <div className="space-y-2">
          <ExistingKnowledge existing={data.existing} />
          <p className="px-1 text-sm text-ink-subtle">{t("encounterHistoryNote")}</p>
        </div>

        {data.documents_today.length > 0 && (
          <Card>
            <CardHeader title={t("encounterDocsToday")} icon={<FileText className="h-5 w-5" />} />
            <CardBody>
              <ul className="space-y-2">
                {data.documents_today.map((document) => (
                  <li key={document.id} className="flex items-center justify-between gap-3">
                    <span className="text-base text-ink">{document.title}</span>
                    <Badge tone="neutral">{v(document.status)}</Badge>
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>
        )}

        {/* Summary for the care team */}
        <Card>
          <CardHeader
            title={t("encounterSummary")}
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

        {/* Explicit confirmation before submission */}
        <Card>
          <CardHeader title={t("encounterConfirmHeading")} icon={<History className="h-5 w-5" />} />
          <CardBody className="space-y-3">
            {confirmRow("symptoms_correct", t("encounterConfirmSymptoms"))}
            {confirmRow("reviewed_information", t("encounterConfirmReviewed"))}
            {confirmRow("understands_use", t("encounterConfirmUnderstands"))}

            {submit.error && (
              <Alert tone="danger">
                {submit.error instanceof ApiError ? submit.error.message : t("errorGeneric")}
              </Alert>
            )}

            <Button
              size={isEasyMode ? "xl" : "lg"}
              block
              disabled={!allConfirmed || submit.isPending}
              onClick={() => submit.mutate()}
            >
              {submit.isPending ? t("encounterSubmitting") : t("encounterSubmit")}
            </Button>
            <Button variant="ghost" size="md" block onClick={() => navigate("/visit")}>
              {t("encounterEditToday")}
            </Button>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
