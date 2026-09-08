import { useMutation, useQuery } from "@tanstack/react-query";
import { Plus, X } from "lucide-react";
import { useMemo, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { Input } from "@/components/ui/Field";
import { ProgressBar } from "@/components/ui/Progress";
import { LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { iconFor } from "@/features/accessibility/icons";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type {
  MedicalProfile,
  MedicalSectionContent,
} from "@/types/api";

type Draft = Record<string, string[]>;

export function MedicalProfilePage() {
  const { t, s, language } = useI18n();
  const { isEasyMode, isLoading: preferencesLoading } = usePreferences();
  const { advance, isAdvancing } = useAdvance();

  const [draft, setDraft] = useState<Draft | null>(null);
  const [typed, setTyped] = useState<Record<string, string>>({});
  // Easy Mode walks one section at a time.
  const [cursor, setCursor] = useState(0);

  const content = useQuery({
    queryKey: ["medical-content"],
    queryFn: () => api.get<{ sections: MedicalSectionContent[] }>(
      "/patients/me/medical-profile/content",
    ),
    staleTime: Infinity,
  });

  const existing = useQuery({
    queryKey: ["medical-profile"],
    queryFn: () => api.get<MedicalProfile>("/patients/me/medical-profile"),
  });

  const sections = content.data?.sections ?? [];

  // Seed the editable draft from whatever is already saved.
  const workingDraft = useMemo<Draft>(() => {
    if (draft) return draft;
    const seeded: Draft = {};
    for (const section of sections) {
      seeded[section.key] = (existing.data?.sections[section.key] ?? []).map(
        (item) => item.value,
      );
    }
    return seeded;
  }, [draft, sections, existing.data]);

  const itemsIn = (key: string) => workingDraft[key] ?? [];

  const addItem = (key: string, rawValue: string) => {
    const value = rawValue.trim().replace(/\s+/g, " ");
    if (!value) return;
    setDraft({
      ...workingDraft,
      [key]: itemsIn(key).some((item) => item.toLowerCase() === value.toLowerCase())
        ? itemsIn(key)
        : [...itemsIn(key), value],
    });
    setTyped((current) => ({ ...current, [key]: "" }));
  };

  const removeItem = (key: string, value: string) =>
    setDraft({ ...workingDraft, [key]: itemsIn(key).filter((item) => item !== value) });

  const save = useMutation({
    mutationFn: () =>
      api.put<MedicalProfile>("/patients/me/medical-profile", {
        sections: Object.fromEntries(
          sections.map((section) => [
            section.key,
            itemsIn(section.key).map((value) => ({ value })),
          ]),
        ),
      }),
    onSuccess: () => void advance("/onboarding/records"),
  });

  if (content.isLoading || existing.isLoading || preferencesLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  const visible = isEasyMode ? sections.slice(cursor, cursor + 1) : sections;
  const isLastSection = cursor >= sections.length - 1;
  const totalItems = sections.reduce((sum, section) => sum + itemsIn(section.key).length, 0);

  const renderSection = (section: MedicalSectionContent) => (
    <section key={section.key} className="space-y-3">
      <div className="flex items-start gap-3">
        <span
          aria-hidden="true"
          className="mt-0.5 flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-soft text-primary"
        >
          {iconFor(section.icon)}
        </span>
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h2
              className={
                isEasyMode
                  ? "text-2xl font-semibold text-ink"
                  : "text-lg font-semibold text-ink"
              }
            >
              {s(section.title)}
            </h2>
            {section.important && <Badge tone="warning">{t("consentRequiredTag")}</Badge>}
          </div>
          <p className="mt-1 text-base text-ink-muted">{s(section.prompt)}</p>
        </div>
      </div>

      {/* Already-added entries */}
      {itemsIn(section.key).length > 0 && (
        <ul className="flex flex-wrap gap-2">
          {itemsIn(section.key).map((value) => (
            <li key={value}>
              <span className="inline-flex items-center gap-2 rounded-full border-2 border-primary/30 bg-primary-soft px-3 py-1.5 text-base font-medium text-primary-ink">
                {value}
                <button
                  type="button"
                  onClick={() => removeItem(section.key, value)}
                  aria-label={`${t("remove")}: ${value}`}
                  className="rounded-full p-0.5 hover:bg-primary/15"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}

      <form
        className="flex flex-col gap-2 sm:flex-row"
        onSubmit={(event) => {
          event.preventDefault();
          addItem(section.key, typed[section.key] ?? "");
        }}
      >
        <Input
          aria-label={s(section.title)}
          placeholder={s(section.placeholder) || t("medicalAddPlaceholder")}
          value={typed[section.key] ?? ""}
          onChange={(event) =>
            setTyped((current) => ({ ...current, [section.key]: event.target.value }))
          }
        />
        <Button type="submit" variant="secondary" size="md" disabled={!(typed[section.key] ?? "").trim()}>
          <Plus className="h-5 w-5" aria-hidden="true" />
          {t("add")}
        </Button>
      </form>

      {/* Quick-pick suggestions keep this usable for low-literacy patients. */}
      {section.suggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-ink-subtle">{t("medicalQuickAdd")}</p>
          <div className="flex flex-wrap gap-2">
            {section.suggestions.map((suggestion) => {
              const label = s(suggestion);
              const already = itemsIn(section.key).includes(label);
              return (
                <button
                  key={label}
                  type="button"
                  onClick={() => addItem(section.key, label)}
                  disabled={already}
                  className="min-h-[2.75rem] rounded-full border-2 border-line bg-surface px-4 py-2 text-base font-medium text-ink transition-colors hover:border-primary hover:bg-primary-soft disabled:opacity-45"
                >
                  {label}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </section>
  );

  return (
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={5}
        title={t("medicalHeading")}
        description={t("medicalBody")}
        announce={
          isEasyMode && sections[cursor]
            ? `${s(sections[cursor].title)}. ${s(sections[cursor].prompt)}`
            : undefined
        }
        onBack={isEasyMode && cursor > 0 ? () => setCursor((c) => c - 1) : undefined}
        onNext={
          isEasyMode && !isLastSection ? () => setCursor((c) => c + 1) : () => save.mutate()
        }
        nextLabel={isEasyMode && !isLastSection ? t("continue") : t("medicalFinish")}
        isBusy={save.isPending || isAdvancing}
        footerNote={`${totalItems} ${t("medicalItemsAdded")}`}
        aside={
          <Card>
            <CardBody className="space-y-2">
              <p className="text-sm font-semibold text-ink-muted">
                {totalItems} {t("profileItemsRecorded")}
              </p>
              <ProgressBar
                percent={
                  (sections.filter((section) => itemsIn(section.key).length > 0).length /
                    Math.max(1, sections.length)) *
                  100
                }
              />
              <p className="text-sm text-ink-muted">{t("profileNextVisitNote")}</p>
            </CardBody>
          </Card>
        }
      >
        {save.error && (
          <Alert tone="danger">
            {save.error instanceof ApiError ? save.error.message : t("errorGeneric")}
          </Alert>
        )}

        {isEasyMode && (
          <div className="space-y-2">
            <p className="text-sm font-semibold text-ink-muted">
              {t("medicalSectionOf")} {cursor + 1} {t("assessmentOf")} {sections.length}
            </p>
            <ProgressBar percent={((cursor + 1) / sections.length) * 100} />
          </div>
        )}

        <div className={isEasyMode ? "" : "space-y-8"}>{visible.map(renderSection)}</div>
      </StepLayout>
    </AppShell>
  );
}
