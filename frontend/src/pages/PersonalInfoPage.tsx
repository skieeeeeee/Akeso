import { useMutation } from "@tanstack/react-query";
import { CalendarDays, PhoneCall, UserRound } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Dictate } from "@/components/ui/Dictate";
import { Field, Input, Select } from "@/components/ui/Field";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { ApiError, api } from "@/services/apiClient";
import { useAuth } from "@/providers/AuthProvider";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type { Gender, Language, Patient, PersonalInfoPayload } from "@/types/api";
import { LANGUAGE_LABELS } from "@/providers/I18nProvider";

/** Age derived locally purely to reassure the patient the date is right. */
function ageFrom(dateOfBirth: string): number | null {
  if (!dateOfBirth) return null;
  const dob = new Date(dateOfBirth);
  if (Number.isNaN(dob.getTime())) return null;
  const today = new Date();
  let years = today.getFullYear() - dob.getFullYear();
  const monthDay = today.getMonth() * 100 + today.getDate();
  const dobMonthDay = dob.getMonth() * 100 + dob.getDate();
  if (monthDay < dobMonthDay) years -= 1;
  return years >= 0 && years < 130 ? years : null;
}

const GENDERS: Array<{ value: Gender; key: "genderMale" | "genderFemale" | "genderOther" | "genderUndisclosed" }> = [
  { value: "male", key: "genderMale" },
  { value: "female", key: "genderFemale" },
  { value: "other", key: "genderOther" },
  { value: "undisclosed", key: "genderUndisclosed" },
];

export function PersonalInfoPage() {
  const { t, language, setLanguage } = useI18n();
  const { session } = useAuth();
  const { isEasyMode } = usePreferences();
  const { advance, isAdvancing } = useAdvance();
  const navigate = useNavigate();
  const patient = session!.patient;

  const [form, setForm] = useState({
    full_name: patient.full_name ?? "",
    date_of_birth: patient.date_of_birth ?? "",
    gender: (patient.gender ?? "") as Gender | "",
    preferred_language: patient.preferred_language,
    emergency_contact_name: patient.emergency_contact_name ?? "",
    emergency_contact_number: patient.emergency_contact_number ?? "",
    emergency_contact_relation: patient.emergency_contact_relation ?? "",
  });

  const age = useMemo(() => ageFrom(form.date_of_birth), [form.date_of_birth]);
  const set = <K extends keyof typeof form>(key: K, value: (typeof form)[K]) =>
    setForm((current) => ({ ...current, [key]: value }));

  const save = useMutation({
    mutationFn: () => {
      const payload: PersonalInfoPayload = {
        full_name: form.full_name.trim() || null,
        date_of_birth: form.date_of_birth || null,
        gender: form.gender || null,
        preferred_language: form.preferred_language,
        emergency_contact_name: form.emergency_contact_name.trim() || null,
        emergency_contact_number: form.emergency_contact_number.trim() || null,
        emergency_contact_relation: form.emergency_contact_relation.trim() || null,
      };
      return api.patch<Patient>("/patients/me", payload);
    },
    onSuccess: () => void advance("/onboarding/assessment"),
  });

  const message = save.error instanceof ApiError ? save.error.message : null;
  const complete = Boolean(form.full_name.trim() && form.date_of_birth && form.gender);

  return (
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={1}
        title={t("personalHeading")}
        description={t("personalBody")}
        onNext={() => save.mutate()}
        onBack={() => navigate("/onboarding/abha")}
        nextDisabled={!complete}
        isBusy={save.isPending || isAdvancing}
        footerNote={t("progressSavedNote")}
        aside={
          <Card>
            <CardHeader title={t("emergencyHeading")} icon={<PhoneCall className="h-5 w-5" />} />
            <CardBody>
              <p className="text-sm text-ink-muted">{t("emergencyBody")}</p>
            </CardBody>
          </Card>
        }
      >
        {message && <Alert tone="danger">{message}</Alert>}

        <Field label={t("fullNameLabel")} hint={t("fullNameHint")} required>
          {({ inputId, describedBy }) => (
            <div className="space-y-2">
              <Input
                id={inputId}
                aria-describedby={describedBy}
                autoComplete="name"
                value={form.full_name}
                onChange={(event) => set("full_name", event.target.value)}
              />
              {/* The very first field in the product. A patient who cannot
                  type should not be stopped at their own name. */}
              <Dictate
                label={t("fullNameLabel")}
                onText={(said) =>
                  set("full_name", [form.full_name, said].filter(Boolean).join(" ").trim())
                }
              />
            </div>
          )}
        </Field>

        <Field label={t("dobLabel")} hint={t("dobHint")} required>
          {({ inputId, describedBy }) => (
            <div className="flex flex-wrap items-center gap-3">
              <Input
                id={inputId}
                aria-describedby={describedBy}
                type="date"
                max={new Date().toISOString().slice(0, 10)}
                value={form.date_of_birth}
                onChange={(event) => set("date_of_birth", event.target.value)}
                className="max-w-[16rem]"
              />
              {age !== null && (
                <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-soft px-3 py-1.5 text-sm font-semibold text-primary-ink">
                  <CalendarDays className="h-4 w-4" aria-hidden="true" />
                  {t("ageIs")}: {age} {t("years")}
                </span>
              )}
            </div>
          )}
        </Field>

        <fieldset className="space-y-2">
          <legend className="block text-base font-semibold text-ink">
            {t("genderLabel")}
            <span className="ml-1 text-danger" aria-hidden="true">*</span>
          </legend>
          <OptionGrid columns={isEasyMode ? 1 : 2}>
            {GENDERS.map((option) => (
              <OptionCard
                key={option.value}
                name="gender"
                value={option.value}
                checked={form.gender === option.value}
                onSelect={(value) => set("gender", value as Gender)}
                label={t(option.key)}
              />
            ))}
          </OptionGrid>
        </fieldset>

        <Field label={t("languageLabel")}>
          {({ inputId }) => (
            <Select
              id={inputId}
              value={form.preferred_language}
              onChange={(event) => {
                const next = event.target.value as Language;
                set("preferred_language", next);
                setLanguage(next);
              }}
              className="max-w-[16rem]"
            >
              {(Object.keys(LANGUAGE_LABELS) as Language[]).map((code) => (
                <option key={code} value={code}>
                  {LANGUAGE_LABELS[code].native}
                </option>
              ))}
            </Select>
          )}
        </Field>

        <div className="space-y-4 rounded-2xl border border-line bg-surface-muted p-4 sm:p-5">
          <div className="flex items-center gap-2">
            <UserRound className="h-5 w-5 text-primary" aria-hidden="true" />
            <h2 className="text-base font-semibold text-ink">{t("emergencyHeading")}</h2>
          </div>

          <Field label={t("emergencyNameLabel")}>
            {({ inputId }) => (
              <div className="space-y-2">
                <Input
                  id={inputId}
                  autoComplete="off"
                  value={form.emergency_contact_name}
                  onChange={(event) => set("emergency_contact_name", event.target.value)}
                />
                <Dictate
                  label={t("emergencyNameLabel")}
                  onText={(said) =>
                    set(
                      "emergency_contact_name",
                      [form.emergency_contact_name, said].filter(Boolean).join(" ").trim(),
                    )
                  }
                />
              </div>
            )}
          </Field>

          <Field label={t("emergencyNumberLabel")}>
            {({ inputId }) => (
              <Input
                id={inputId}
                type="tel"
                inputMode="numeric"
                value={form.emergency_contact_number}
                onChange={(event) => set("emergency_contact_number", event.target.value)}
                placeholder="98765 43210"
              />
            )}
          </Field>

          <Field label={t("emergencyRelationLabel")} hint={t("emergencyRelationHint")}>
            {({ inputId, describedBy }) => (
              <div className="space-y-2">
                <Input
                  id={inputId}
                  aria-describedby={describedBy}
                  value={form.emergency_contact_relation}
                  onChange={(event) => set("emergency_contact_relation", event.target.value)}
                />
                <Dictate
                  label={t("emergencyRelationLabel")}
                  onText={(said) =>
                    set(
                      "emergency_contact_relation",
                      [form.emergency_contact_relation, said].filter(Boolean).join(" ").trim(),
                    )
                  }
                />
              </div>
            )}
          </Field>
        </div>
      </StepLayout>
    </AppShell>
  );
}
