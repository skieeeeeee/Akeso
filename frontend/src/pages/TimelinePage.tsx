import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  CalendarClock,
  FileText,
  FlaskConical,
  Pill,
  Scissors,
  Stethoscope,
  TriangleAlert,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { EmptyState, ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { LAB_FLAG_TONE, labFlagLabel, sourceSentence } from "@/lib/enumLabels";
import type { Timeline, TimelineEventType } from "@/types/api";

const EVENT_META: Record<
  TimelineEventType,
  { icon: typeof FileText; label: { en: string; hi: string } }
> = {
  document: { icon: FileText, label: { en: "Records", hi: "रिकॉर्ड" } },
  diagnosis: { icon: Stethoscope, label: { en: "Conditions", hi: "बीमारियाँ" } },
  medication: { icon: Pill, label: { en: "Medicines", hi: "दवाइयाँ" } },
  investigation: { icon: FlaskConical, label: { en: "Tests", hi: "जाँचें" } },
  surgery: { icon: Scissors, label: { en: "Operations", hi: "ऑपरेशन" } },
  visit: { icon: Activity, label: { en: "Visits", hi: "मुलाक़ातें" } },
};

export function TimelinePage() {
  const { t, s, v, language } = useI18n();
  const [filter, setFilter] = useState<TimelineEventType | null>(null);

  const timeline = useQuery({
    queryKey: ["timeline", filter],
    queryFn: () =>
      api.get<Timeline>(`/timeline${filter ? `?event_type=${filter}` : ""}`),
  });


  if (timeline.isLoading) {
    return (
      <AppShell wide>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (timeline.isError || !timeline.data) {
    return (
      <AppShell wide>
        <ErrorPanel
          message={timeline.error instanceof ApiError ? timeline.error.message : t("errorNetwork")}
          onRetry={() => void timeline.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const { events, counts, disclaimer } = timeline.data;
  // Only offer filters that would return something.
  const available = (Object.keys(EVENT_META) as TimelineEventType[]).filter(
    (type) => (counts[type] ?? 0) > 0,
  );

  return (
    <AppShell wide backRoute="/home" backLabel={t("backToHome")}>
      <div className="space-y-5">
        <div>
          <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("timelineHeading")}</h1>
          <p className="mt-1 text-base text-ink-muted">{t("timelineBody")}</p>
        </div>

        <Alert tone="info">{s(disclaimer)}</Alert>

        {available.length > 0 && (
          <div className="flex flex-wrap gap-2" role="group" aria-label={t("timelineAll")}>
            <button
              type="button"
              onClick={() => setFilter(null)}
              aria-pressed={filter === null}
              className={cn(
                "min-h-[2.75rem] rounded-full border-2 px-4 py-2 text-base font-semibold transition-colors",
                filter === null
                  ? "border-primary bg-primary text-white"
                  : "border-line bg-surface text-ink hover:border-primary",
              )}
            >
              {t("timelineAll")}
            </button>
            {available.map((type) => {
              const Icon = EVENT_META[type].icon;
              return (
                <button
                  key={type}
                  type="button"
                  onClick={() => setFilter(type)}
                  aria-pressed={filter === type}
                  className={cn(
                    "inline-flex min-h-[2.75rem] items-center gap-2 rounded-full border-2 px-4 py-2 text-base font-semibold transition-colors",
                    filter === type
                      ? "border-primary bg-primary text-white"
                      : "border-line bg-surface text-ink hover:border-primary",
                  )}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  {s(EVENT_META[type].label)}
                  <span className="text-sm opacity-80">{counts[type]}</span>
                </button>
              );
            })}
          </div>
        )}

        {events.length === 0 ? (
          <EmptyState
            icon={<CalendarClock className="h-6 w-6" />}
            title={t("timelineEmptyTitle")}
            description={t("timelineEmptyBody")}
            action={
              <Button asChild>
                <Link to="/interview">{t("interviewStart")}</Link>
              </Button>
            }
          />
        ) : (
          <ol className="space-y-3">
            {events.map((event) => {
              const Icon = EVENT_META[event.event_type].icon;
              return (
                <li key={event.id}>
                  <Card>
                    <CardBody className="flex items-start gap-4">
                      <span
                        aria-hidden="true"
                        className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"
                      >
                        <Icon className="h-5 w-5" />
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <p className="font-semibold text-ink">{event.title}</p>
                          {event.flag && (
                            <Badge tone={LAB_FLAG_TONE[event.flag]}>
                              {labFlagLabel(event.flag, language)}
                            </Badge>
                          )}
                          {event.requires_review && (
                            <Badge
                              tone="warning"
                              icon={<TriangleAlert className="h-3.5 w-3.5" />}
                            >
                              {t("timelineNeedsCheck")}
                            </Badge>
                          )}
                        </div>
                        {(event.detail || event.detail_kind) && (
                          <p className="mt-0.5 text-base text-ink-muted">
                            {event.detail_kind ? v(event.detail_kind) : event.detail}
                          </p>
                        )}
                        {/* Provenance is always stated. */}
                        <p className="mt-1 text-sm text-ink-subtle">
                          {sourceSentence(event.source_kind, event.source_name, language)}
                        </p>
                      </div>
                      <p className="shrink-0 text-sm font-medium text-ink-muted">
                        {event.event_date
                          ? new Date(event.event_date).toLocaleDateString(
                              language === "hi" ? "hi-IN" : "en-IN",
                              { day: "2-digit", month: "short", year: "numeric" },
                            )
                          : t("timelineNoDate")}
                      </p>
                    </CardBody>
                  </Card>
                </li>
              );
            })}
          </ol>
        )}

        <p className="text-center text-xs text-ink-subtle">{t("labDisclaimer")}</p>
      </div>
    </AppShell>
  );
}
