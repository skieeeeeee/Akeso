import { Link } from "react-router-dom";
import { CalendarClock, CheckCircle2, IdCard, ListChecks } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/Badge";
import { api } from "@/services/apiClient";
import { useAuth } from "@/providers/AuthProvider";
import { useI18n } from "@/providers/I18nProvider";
import { PROFILE_PATH } from "@/features/onboarding/steps";
import type { PatientProfile } from "@/types/api";

export function CompletePage() {
  const { t, v } = useI18n();
  const { session } = useAuth();

  const profile = useQuery({
    queryKey: ["patient-profile"],
    queryFn: () => api.get<PatientProfile>("/patients/me/profile"),
  });

  const patient = profile.data?.patient ?? session?.patient;

  return (
    <AppShell>
      <div className="space-y-5">
        <Card>
          <CardBody className="space-y-6 py-9 text-center">
            <span
              aria-hidden="true"
              className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-success-soft text-success"
            >
              <CheckCircle2 className="h-11 w-11" />
            </span>

            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-ink">{t("completeHeading")}</h1>
              <p className="mx-auto max-w-xl text-lg text-ink-muted">{t("completeBody")}</p>
            </div>

            {/* A real summary, so the screen is useful rather than a dead end. */}
            {patient && (
              <dl className="mx-auto grid max-w-xl gap-3 text-left sm:grid-cols-2">
                <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
                  <dt className="text-sm text-ink-muted">{t("fullNameLabel")}</dt>
                  <dd className="text-lg font-semibold text-ink">{patient.display_name}</dd>
                </div>
                <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
                  <dt className="text-sm text-ink-muted">{t("ageIs")}</dt>
                  <dd className="text-lg font-semibold text-ink">
                    {patient.age !== null ? `${patient.age} ${t("years")}` : t("notProvided")}
                  </dd>
                </div>
                <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
                  <dt className="flex items-center gap-1.5 text-sm text-ink-muted">
                    <IdCard className="h-4 w-4" aria-hidden="true" />
                    {t("profileHealthId")}
                  </dt>
                  <dd className="mt-1">
                    {profile.data?.abha ? (
                      <StatusBadge
                        status={profile.data.abha.verification_status}
                        label={v(profile.data.abha.verification_status)}
                      />
                    ) : (
                      <span className="text-base text-ink-muted">{t("notProvided")}</span>
                    )}
                  </dd>
                </div>
                <div className="rounded-xl border border-line bg-surface-muted px-4 py-3">
                  <dt className="flex items-center gap-1.5 text-sm text-ink-muted">
                    <ListChecks className="h-4 w-4" aria-hidden="true" />
                    {t("profileHistory")}
                  </dt>
                  <dd className="text-lg font-semibold text-ink">
                    {profile.data?.medical_profile.total_items ?? 0} {t("profileItemsRecorded")}
                  </dd>
                </div>
              </dl>
            )}

            <div className="mx-auto flex w-full max-w-form flex-col gap-3">
              {/* Onboarding done; the medical interview is the natural next step. */}
              <Button size="xl" asChild>
                <Link to="/interview">{t("interviewStart")}</Link>
              </Button>
              <Button size="lg" variant="secondary" asChild>
                <Link to={PROFILE_PATH}>{t("completeViewProfile")}</Link>
              </Button>
            </div>
          </CardBody>
        </Card>

        <Card className="border-primary/25 bg-primary-soft">
          <CardBody className="flex items-start gap-3">
            <CalendarClock className="mt-0.5 h-6 w-6 shrink-0 text-primary" aria-hidden="true" />
            <p className="text-base text-primary-ink">{t("profileNextVisitNote")}</p>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
