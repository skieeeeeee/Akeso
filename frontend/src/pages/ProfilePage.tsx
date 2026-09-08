import { useQuery } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router-dom";
import {
  BookOpen,
  CalendarClock,
  FileText,
  IdCard,
  ListChecks,
  Settings2,
  ShieldCheck,
  UserRound,
} from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Badge, StatusBadge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import type { MedicalProfile, PatientProfile } from "@/types/api";

const SECTION_TITLES: Record<string, { en: string; hi: string }> = {
  past_medical_history: { en: "Past illnesses", hi: "पिछली बीमारियाँ" },
  current_medications: { en: "Medicines", hi: "दवाइयाँ" },
  allergies: { en: "Allergies", hi: "एलर्जी" },
  surgical_history: { en: "Operations", hi: "ऑपरेशन" },
  family_history: { en: "Family history", hi: "पारिवारिक इतिहास" },
  personal_history: { en: "Daily habits", hi: "दैनिक आदतें" },
  previous_investigations: { en: "Test results", hi: "जाँच परिणाम" },
  additional_information: { en: "Other notes", hi: "अन्य टिप्पणियाँ" },
};

export function ProfilePage() {
  const { t, s, v } = useI18n();
  const navigate = useNavigate();

  const profile = useQuery({
    queryKey: ["patient-profile"],
    queryFn: () => api.get<PatientProfile>("/patients/me/profile"),
  });

  const medical = useQuery({
    queryKey: ["medical-profile"],
    queryFn: () => api.get<MedicalProfile>("/patients/me/medical-profile"),
  });

  if (profile.isLoading) {
    return (
      <AppShell wide>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (profile.isError || !profile.data) {
    return (
      <AppShell wide>
        <ErrorPanel
          message={profile.error instanceof ApiError ? profile.error.message : t("errorNetwork")}
          onRetry={() => void profile.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const { patient, onboarding, abha, preferences, consents, medical_profile, document_count, encounter_count } =
    profile.data;

  const sectionsWithItems = Object.entries(medical.data?.sections ?? {}).filter(
    ([, items]) => items.length > 0,
  );

  return (
    <AppShell wide>
      <div className="space-y-5">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("profileHeading")}</h1>
            <p className="mt-1 text-base text-ink-muted">{t("profileNextVisitNote")}</p>
          </div>
          {patient.is_demo && <Badge tone="warning">{t("demoPatientBadge")}</Badge>}
        </div>

        {/* Never a dead end: an unfinished profile says exactly what to do. */}
        {!onboarding.is_complete && (
          <Alert
            tone="warning"
            title={t("profileIncompleteNotice")}
            action={{
              label: t("profileFinishOnboarding"),
              onClick: () => navigate(onboarding.next_route),
            }}
          />
        )}

        <div className="grid gap-5 lg:grid-cols-[1.4fr_1fr]">
          <div className="space-y-5">
            <Card>
              <CardHeader title={t("profileIdentity")} icon={<UserRound className="h-5 w-5" />} />
              <CardBody>
                <dl className="grid gap-4 sm:grid-cols-2">
                  {[
                    [t("fullNameLabel"), patient.display_name],
                    [
                      t("ageIs"),
                      patient.age !== null ? `${patient.age} ${t("years")}` : t("notProvided"),
                    ],
                    [t("genderLabel"), patient.gender ? v(patient.gender) : t("notProvided")],
                    [t("mobileLabel"), patient.mobile_number],
                    [
                      t("emergencyNameLabel"),
                      patient.emergency_contact_name
                        ? `${patient.emergency_contact_name}${
                            patient.emergency_contact_relation
                              ? ` (${patient.emergency_contact_relation})`
                              : ""
                          }`
                        : t("notProvided"),
                    ],
                    [
                      t("emergencyNumberLabel"),
                      patient.emergency_contact_number ?? t("notProvided"),
                    ],
                  ].map(([label, value]) => (
                    <div key={label}>
                      <dt className="text-sm text-ink-muted">{label}</dt>
                      <dd className="text-base font-semibold capitalize text-ink">{value}</dd>
                    </div>
                  ))}
                </dl>
              </CardBody>
            </Card>

            <Card className="border-primary/25 bg-primary-soft">
              <CardBody className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="font-semibold text-primary-ink">{t("interviewHeading")}</p>
                  <p className="text-sm text-primary-ink/80">{t("interviewIntro")}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button asChild>
                    <Link to="/interview">{t("interviewStart")}</Link>
                  </Button>
                  <Button variant="secondary" asChild>
                    <Link to="/timeline">{t("timelineHeading")}</Link>
                  </Button>
                  <Button variant="secondary" asChild>
                    <Link to="/review">{t("reviewHeading")}</Link>
                  </Button>
                </div>
              </CardBody>
            </Card>

            <Card>
              <CardHeader
                title={t("profileHistory")}
                description={`${medical_profile.total_items} ${t("profileItemsRecorded")}`}
                icon={<ListChecks className="h-5 w-5" />}
                action={
                  <Button variant="secondary" size="md" asChild>
                    <Link to="/onboarding/medical-profile">{t("edit")}</Link>
                  </Button>
                }
              />
              <CardBody>
                {sectionsWithItems.length === 0 ? (
                  <p className="text-base text-ink-muted">{t("medicalNothingToAdd")}</p>
                ) : (
                  <dl className="space-y-4">
                    {sectionsWithItems.map(([key, items]) => (
                      <div key={key}>
                        <dt className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">
                          {SECTION_TITLES[key] ? s(SECTION_TITLES[key]) : v(key)}
                        </dt>
                        <dd className="mt-1.5 flex flex-wrap gap-2">
                          {items.map((item) => (
                            <span
                              key={`${key}-${item.value}`}
                              className="rounded-full border border-line bg-surface-muted px-3 py-1.5 text-base text-ink"
                            >
                              {item.value}
                              {item.attributes.dose ? ` · ${item.attributes.dose}` : ""}
                              {item.attributes.frequency ? ` · ${item.attributes.frequency}` : ""}
                            </span>
                          ))}
                        </dd>
                      </div>
                    ))}
                  </dl>
                )}
              </CardBody>
            </Card>
          </div>

          <div className="space-y-5">
            <Card>
              <CardHeader title={t("profileHealthId")} icon={<IdCard className="h-5 w-5" />} />
              <CardBody className="space-y-3">
                {abha?.abha_id ? (
                  <>
                    <p className="break-all font-mono text-lg text-ink">{abha.abha_id}</p>
                    <StatusBadge
                      status={abha.verification_status}
                      label={v(abha.verification_status)}
                    />
                    {abha.is_mock && (
                      <p className="text-xs text-ink-subtle">{t("abhaMockNotice")}</p>
                    )}
                  </>
                ) : (
                  <>
                    <p className="text-base text-ink-muted">{t("notProvided")}</p>
                    <Button variant="secondary" size="md" asChild>
                      <Link to="/onboarding/abha">{t("abhaConnect")}</Link>
                    </Button>
                  </>
                )}
              </CardBody>
            </Card>

            <Card>
              <CardHeader
                title={t("profileExperience")}
                icon={<Settings2 className="h-5 w-5" />}
                action={
                  <Button variant="secondary" size="md" asChild>
                    <Link to="/onboarding/preferences">{t("edit")}</Link>
                  </Button>
                }
              />
              <CardBody>
                {preferences ? (
                  <dl className="space-y-2 text-base">
                    {[
                      [t("interfaceModeLabel"), v(preferences.interface_mode)],
                      [t("fontSizeLabel"), v(preferences.font_size)],
                      [t("contrastLabel"), v(preferences.contrast_mode)],
                      [t("interactionLabel"), v(preferences.interaction_preference)],
                      [t("audioGuidanceLabel"), preferences.audio_guidance ? t("yes") : t("no")],
                    ].map(([label, value]) => (
                      <div key={label} className="flex items-center justify-between gap-3">
                        <dt className="text-ink-muted">{label}</dt>
                        <dd className="font-semibold capitalize text-ink">{value}</dd>
                      </div>
                    ))}
                  </dl>
                ) : (
                  <p className="text-base text-ink-muted">{t("notProvided")}</p>
                )}
                <p className="mt-3 text-xs text-ink-subtle">{t("neverLockedNote")}</p>
              </CardBody>
            </Card>

            <Card>
              <CardHeader
                title={t("ayushOpenTitle")}
                description={t("ayushOpenBody")}
                icon={<BookOpen className="h-5 w-5" />}
                action={
                  <Button variant="secondary" size="md" asChild>
                    <Link to="/ayush">{t("edit")}</Link>
                  </Button>
                }
              />
            </Card>

            <Card>
              <CardHeader title={t("profileConsents")} icon={<ShieldCheck className="h-5 w-5" />} />
              <CardBody>
                {consents.length === 0 ? (
                  <p className="text-base text-ink-muted">{t("notProvided")}</p>
                ) : (
                  <ul className="space-y-2">
                    {consents.map((consent) => (
                      <li
                        key={consent.purpose}
                        className="flex items-center justify-between gap-3 text-base"
                      >
                        <span className="text-ink-muted">
                          {v(consent.purpose)}
                        </span>
                        <StatusBadge status={consent.status} label={v(consent.status)} />
                      </li>
                    ))}
                  </ul>
                )}
              </CardBody>
            </Card>

            <div className="grid grid-cols-2 gap-3">
              <Card>
                <CardBody className="space-y-1">
                  <p className="flex items-center gap-1.5 text-sm text-ink-muted">
                    <FileText className="h-4 w-4" aria-hidden="true" />
                    {t("profileRecords")}
                  </p>
                  <p className="text-2xl font-bold text-ink">{document_count}</p>
                  <Button variant="ghost" size="md" asChild className="px-0">
                    <Link to="/records">{t("add")}</Link>
                  </Button>
                </CardBody>
              </Card>
              <Card>
                <CardBody className="space-y-1">
                  <p className="flex items-center gap-1.5 text-sm text-ink-muted">
                    <CalendarClock className="h-4 w-4" aria-hidden="true" />
                    {t("profileVisits")}
                  </p>
                  <p className="text-2xl font-bold text-ink">{encounter_count}</p>
                  {encounter_count === 0 && (
                    <p className="text-xs text-ink-subtle">{t("profileNoVisits")}</p>
                  )}
                </CardBody>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
