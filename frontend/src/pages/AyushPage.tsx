import { useMutation, useQuery } from "@tanstack/react-query";
import { BookOpen, CheckCircle2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Dictate } from "@/components/ui/Dictate";
import { Field, Textarea } from "@/components/ui/Field";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { ProgressBar } from "@/components/ui/Progress";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import type { AyushAssessment, AyushContent } from "@/types/api";

/**
 * Dashavidha Pariksha plus Ahara/Vihara.
 *
 * Entirely optional: every factor can be left blank and the whole screen can
 * be skipped, which is why it is not part of the guarded onboarding sequence.
 */
export function AyushPage() {
  const { t, s } = useI18n();
  const { isEasyMode } = usePreferences();
  const navigate = useNavigate();

  const [dashavidha, setDashavidha] = useState<Record<string, string>>({});
  const [ashtasthana, setAshtasthana] = useState<Record<string, string>>({});
  const [lifestyle, setLifestyle] = useState<Record<string, string>>({});
  const [ahara, setAhara] = useState<string[]>([]);
  const [vihara, setVihara] = useState<string[]>([]);
  const [notes, setNotes] = useState("");

  const content = useQuery({
    queryKey: ["ayush-content"],
    queryFn: () => api.get<AyushContent>("/ayush/content"),
    staleTime: Infinity,
  });

  const existing = useQuery({
    queryKey: ["ayush"],
    queryFn: () => api.get<AyushAssessment | null>("/ayush"),
  });

  // Seed from whatever was saved before, so returning here is not a reset.
  useEffect(() => {
    if (!existing.data) return;
    setDashavidha(existing.data.dashavidha ?? {});
    setAshtasthana(existing.data.ashtasthana ?? {});
    setLifestyle(existing.data.lifestyle ?? {});
    setAhara(existing.data.ahara ?? []);
    setVihara(existing.data.vihara ?? []);
    setNotes(existing.data.notes ?? "");
  }, [existing.data]);

  const save = useMutation({
    mutationFn: () =>
      api.put<AyushAssessment>("/ayush", {
        dashavidha,
        ashtasthana,
        lifestyle,
        ahara,
        vihara,
        notes,
      }),
    onSuccess: () => navigate("/review"),
  });

  if (content.isLoading || existing.isLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (content.isError || !content.data) {
    return (
      <AppShell>
        <ErrorPanel
          message={content.error instanceof ApiError ? content.error.message : t("errorNetwork")}
          onRetry={() => void content.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const data = content.data;
  const answered =
    [...Object.values(dashavidha), ...Object.values(ashtasthana), ...Object.values(lifestyle)]
      .filter(Boolean).length +
    (ahara.length > 0 ? 1 : 0) +
    (vihara.length > 0 ? 1 : 0);

  const toggle = (list: string[], value: string) =>
    list.includes(value) ? list.filter((entry) => entry !== value) : [...list, value];

  // The three examination groups, rendered identically.
  const GROUPS = [
    {
      key: "dashavidha",
      title: t("ayushDashavidha"),
      help: t("ayushDashavidhaHelp"),
      factors: data.dashavidha,
      answers: dashavidha,
      set: setDashavidha,
    },
    {
      key: "ashtasthana",
      title: t("ayushAshtasthana"),
      help: t("ayushAshtasthanaHelp"),
      factors: data.ashtasthana,
      answers: ashtasthana,
      set: setAshtasthana,
    },
    {
      key: "lifestyle",
      title: t("ayushLifestyle"),
      help: t("ayushLifestyleHelp"),
      factors: data.lifestyle,
      answers: lifestyle,
      set: setLifestyle,
    },
  ] as const;

  return (
    <AppShell wide backRoute="/home" backLabel={t("backToHome")}>
      <div className="space-y-5">
        {/* The page's own heading. A CardHeader renders an h2, so without
            this the page had no h1 and screen-reader users had no title. */}
        <h1 className="text-2xl font-bold text-ink sm:text-3xl">{t("ayushHeading")}</h1>

        <Card>
          <CardHeader
            title={s(data.intro.title)}
            description={s(data.intro.body)}
            icon={<BookOpen className="h-5 w-5" />}
          />
          <CardBody className="space-y-3">
            <ProgressBar
              percent={(answered / Math.max(1, data.total_factors)) * 100}
              label={`${answered} / ${data.total_factors} ${t("ayushProgress")}`}
            />
            <p className="text-sm text-ink-subtle">{t("ayushNotDiagnostic")}</p>
          </CardBody>
        </Card>

        {save.error && (
          <Alert tone="danger">
            {save.error instanceof ApiError ? save.error.message : t("errorGeneric")}
          </Alert>
        )}

        {GROUPS.map((group) => (
          <section key={group.key} aria-labelledby={`group-${group.key}`} className="space-y-4">
            <div>
              <h2 id={`group-${group.key}`} className="text-xl font-bold text-ink">
                {group.title}
              </h2>
              <p className="mt-1 text-base text-ink-muted">{group.help}</p>
            </div>

            {group.factors.map((factor) => (
              <Card key={factor.key}>
                <CardBody>
                  <fieldset className="space-y-3">
                    <legend className="space-y-1">
                      <span className="block text-lg font-semibold text-ink">
                        {s(factor.prompt)}
                        <span className="ml-2 text-sm font-normal text-ink-subtle">
                          {s(factor.term)} · {t("optional")}
                        </span>
                      </span>
                      <span className="block text-base text-ink-muted">{s(factor.help)}</span>
                    </legend>
                    <OptionGrid columns={isEasyMode ? 1 : 2}>
                      {factor.options.map((option) => (
                        <OptionCard
                          key={option.value}
                          name={factor.key}
                          value={option.value}
                          checked={group.answers[factor.key] === option.value}
                          label={s(option.label)}
                          onSelect={(value) =>
                            group.set((current) => ({
                              ...current,
                              // Tapping the chosen option clears it, since
                              // every factor is skippable.
                              [factor.key]: current[factor.key] === value ? "" : value,
                            }))
                          }
                        />
                      ))}
                    </OptionGrid>
                  </fieldset>
                </CardBody>
              </Card>
            ))}
          </section>
        ))}

        <Card>
          <CardHeader title={t("ayushAhara")} />
          <CardBody>
            <OptionGrid columns={isEasyMode ? 1 : 2}>
              {data.ahara_options.map((option) => (
                <OptionCard
                  key={option.value}
                  name="ahara"
                  value={option.value}
                  multiple
                  checked={ahara.includes(option.value)}
                  label={s(option.label)}
                  onSelect={(value) => setAhara((current) => toggle(current, value))}
                />
              ))}
            </OptionGrid>
          </CardBody>
        </Card>

        <Card>
          <CardHeader title={t("ayushVihara")} />
          <CardBody>
            <OptionGrid columns={isEasyMode ? 1 : 2}>
              {data.vihara_options.map((option) => (
                <OptionCard
                  key={option.value}
                  name="vihara"
                  value={option.value}
                  multiple
                  checked={vihara.includes(option.value)}
                  label={s(option.label)}
                  onSelect={(value) => setVihara((current) => toggle(current, value))}
                />
              ))}
            </OptionGrid>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <Field label={t("medicalHeading")} hint={t("optional")}>
              {({ inputId }) => (
                <div className="space-y-2">
                  <Textarea
                    id={inputId}
                    rows={3}
                    value={notes}
                    onChange={(event) => setNotes(event.target.value)}
                  />
                  {/* The longest free text in onboarding, and the one most
                      likely to be described rather than typed. */}
                  <Dictate
                    label={t("medicalHeading")}
                    onText={(said) =>
                      setNotes((current) => [current, said].filter(Boolean).join(" ").trim())
                    }
                  />
                </div>
              )}
            </Field>
          </CardBody>
        </Card>

        <Card>
          <CardBody className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <Button variant="ghost" asChild>
              <Link to="/review">{t("ayushSkip")}</Link>
            </Button>
            <Button size="lg" onClick={() => save.mutate()} disabled={save.isPending}>
              <CheckCircle2 className="h-5 w-5" aria-hidden="true" />
              {save.isPending ? t("saving") : t("save")}
            </Button>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
