import { useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  ArrowRight,
  BookOpen,
  CalendarClock,
  ClipboardList,
  FileText,
  Pill,
  PlusCircle,
  Stethoscope,
} from "lucide-react";
import { Link } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge, StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { EmptyState, ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { sourceSentence } from "@/lib/enumLabels";
import { usePreferences } from "@/providers/PreferencesProvider";
import { UrgentBanner } from "@/features/encounter/SafetyScreen";
import type { PatientHome } from "@/types/api";

/**
 * The returning-patient home screen.
 *
 * The point of the whole product is visible here: the patient's history is
 * shown back to them as *context*, and the only thing asked of them is what
 * is wrong today. Nothing on this screen re-collects information.
 */
export function HomePage() {
  const { t, s, v, language } = useI18n();
  const { isEasyMode } = usePreferences();

  const home = useQuery({
    queryKey: ["home"],
    queryFn: () => api.get<PatientHome>("/patients/me/home"),
  });

  if (home.isLoading) {
    return (
      <AppShell wide>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (home.isError || !home.data) {
    return (
      <AppShell wide>
        <ErrorPanel
          message={home.error instanceof ApiError ? home.error.message : t("errorNetwork")}
          onRetry={() => void home.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const data = home.data;
  const formatDate = (value: string | null) =>
    value
      ? new Date(value).toLocaleDateString(language === "hi" ? "hi-IN" : "en-IN", {
          day: "2-digit",
          month: "short",
          year: "numeric",
        })
      : "";

  /** A list card that is never an empty box. */
  const listCard = (
    title: string,
    icon: React.ReactNode,
    values: string[],
    emptyText: string,
  ) => (
    <Card>
      <CardHeader title={title} icon={icon} />
      <CardBody>
        {values.length > 0 ? (
          <ul className="flex flex-wrap gap-2">
            {values.map((value) => (
              <li
                key={value}
                className="rounded-full border border-line bg-surface-muted px-3 py-1.5 text-base text-ink"
              >
                {value}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-base text-ink-muted">{emptyText}</p>
        )}
      </CardBody>
    </Card>
  );

  return (
    // Settings and Sign out both live in the shell's nav now, so this page
    // no longer supplies its own header controls.
    <AppShell wide>
      <div className="space-y-5">
        {data.visit_in_progress?.is_urgent && <UrgentBanner />}

        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-ink sm:text-3xl">
              {s(data.greeting)}
              {data.patient.full_name ? `, ${data.patient.full_name.split(" ")[0]}` : ""}
            </h1>
            <p className="mt-1 text-base text-ink-muted">
              {data.visit_count > 0
                ? `${data.visit_count} ${t("homeVisitCount")}`
                : t("welcomeBody")}
            </p>
          </div>
          {data.patient.is_demo && <Badge tone="warning">{t("demoPatientBadge")}</Badge>}
        </div>

        {/* An unfinished profile always says what to do about it. */}
        {!data.onboarding.is_complete && (
          <Alert tone="warning" title={t("profileIncompleteNotice")}>
            <Button variant="secondary" size="md" asChild className="mt-2">
              <Link to={data.onboarding.next_route}>{t("homeProfileIncomplete")}</Link>
            </Button>
          </Alert>
        )}

        {/* The primary action. */}
        <Card className="border-primary/30 bg-primary-soft">
          <CardBody className="flex flex-col gap-4 py-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2
                className={
                  isEasyMode
                    ? "text-2xl font-bold text-primary-ink"
                    : "text-xl font-bold text-primary-ink"
                }
              >
                {data.visit_in_progress ? t("homeResumeVisit") : t("homeStartVisit")}
              </h2>
              <p className="mt-1 text-base text-primary-ink/85">{t("homeStartVisitHelp")}</p>
              {data.visit_in_progress?.complaint && (
                <p className="mt-2 text-base font-medium text-primary-ink">
                  “{data.visit_in_progress.complaint}”
                </p>
              )}
            </div>
            <Button size={isEasyMode ? "xl" : "lg"} asChild className="shrink-0">
              <Link to="/visit">
                {data.visit_in_progress ? t("continue") : t("welcomeStart")}
                <ArrowRight className="h-6 w-6" aria-hidden="true" />
              </Link>
            </Button>
          </CardBody>
        </Card>

        {/* Health summary: short, high-value, never a data dump. */}
        <section aria-labelledby="health-summary" className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2 id="health-summary" className="text-lg font-semibold text-ink">
              {t("homeYourHealth")}
            </h2>
            <Button variant="ghost" size="md" asChild>
              <Link to="/review">{t("homeViewAll")}</Link>
            </Button>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            {listCard(
              t("homeConditions"),
              <Stethoscope className="h-5 w-5" />,
              data.conditions,
              t("homeNothingYet"),
            )}
            {listCard(
              t("homeMedications"),
              <Pill className="h-5 w-5" />,
              data.medications,
              t("homeNothingYet"),
            )}
            {listCard(
              t("homeAllergies"),
              <AlertTriangle className="h-5 w-5" />,
              data.allergies,
              t("homeNoAllergies"),
            )}
          </div>

          <Card>
            <CardBody className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-base text-ink-muted">
                {data.history_item_count} {t("profileItemsRecorded")}
              </p>
              <Button variant="secondary" size="md" asChild>
                <Link to="/onboarding/medical-profile">
                  <ClipboardList className="h-5 w-5" aria-hidden="true" />
                  {t("homeUpdateHistory")}
                </Link>
              </Button>
            </CardBody>
          </Card>
        </section>

        {/* AYUSH is reachable from the home screen rather than buried in
            the visit flow — an Ayurvedic patient should not have to hunt. */}
        <Card>
          <CardBody className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <span
                aria-hidden="true"
                className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"
              >
                <BookOpen className="h-5 w-5" />
              </span>
              <div>
                <p className="font-semibold text-ink">{t("ayushOpenTitle")}</p>
                <p className="text-sm text-ink-muted">{t("ayushOpenBody")}</p>
              </div>
            </div>
            <Button variant="secondary" size="md" asChild>
              <Link to="/ayush">{t("ayushOpenAction")}</Link>
            </Button>
          </CardBody>
        </Card>

        <div className="grid gap-4 lg:grid-cols-2">
          {/* Records — with a real action when there are none. */}
          <Card>
            <CardHeader
              title={t("homeRecentRecords")}
              icon={<FileText className="h-5 w-5" />}
              action={
                <Button variant="ghost" size="md" asChild>
                  <Link to="/records">
                    <PlusCircle className="h-5 w-5" aria-hidden="true" />
                    {t("add")}
                  </Link>
                </Button>
              }
            />
            <CardBody>
              {data.recent_documents.length > 0 ? (
                <ul className="space-y-2">
                  {data.recent_documents.map((document) => (
                    <li
                      key={document.id}
                      className="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-line bg-surface-muted px-4 py-3"
                    >
                      <div className="min-w-0">
                        <p className="truncate font-medium text-ink">{document.title}</p>
                        <p className="text-sm text-ink-muted">
                          {v(document.type)}
                          {document.date ? ` · ${formatDate(document.date)}` : ""}
                        </p>
                      </div>
                      <StatusBadge status={document.status} label={v(document.status)} />
                    </li>
                  ))}
                </ul>
              ) : (
                <EmptyState
                  icon={<FileText className="h-6 w-6" />}
                  title={t("homeNoRecordsTitle")}
                  description={t("homeNoRecordsBody")}
                  action={
                    <Button asChild>
                      <Link to="/records">{t("recordsChooseFile")}</Link>
                    </Button>
                  }
                />
              )}
            </CardBody>
          </Card>

          {/* Recent activity, straight from the timeline. */}
          <Card>
            <CardHeader
              title={t("homeRecentActivity")}
              icon={<CalendarClock className="h-5 w-5" />}
              action={
                <Button variant="ghost" size="md" asChild>
                  <Link to="/timeline">{t("homeViewAll")}</Link>
                </Button>
              }
            />
            <CardBody className="space-y-3">
              {data.last_visit && (
                <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
                  <p className="text-sm text-ink-muted">{t("homeLastVisit")}</p>
                  <p className="font-medium text-ink">
                    {data.last_visit.complaint ?? t("homeNothingYet")}
                  </p>
                  <p className="text-sm text-ink-subtle">
                    {formatDate(data.last_visit.submitted_at)}
                  </p>
                </div>
              )}

              {data.recent_events.length > 0 ? (
                <ul className="space-y-2">
                  {data.recent_events.map((event) => (
                    <li key={event.id} className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <p className="truncate text-base text-ink">{event.title}</p>
                        {/* Provenance is always stated. */}
                        <p className="text-sm text-ink-subtle">
                          {sourceSentence(event.source_kind, event.source_name, language)}
                        </p>
                      </div>
                      <p className="shrink-0 whitespace-nowrap text-sm text-ink-muted">
                        {formatDate(event.event_date)}
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <EmptyState
                  icon={<CalendarClock className="h-6 w-6" />}
                  title={t("timelineEmptyTitle")}
                  description={t("timelineEmptyBody")}
                />
              )}
            </CardBody>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
