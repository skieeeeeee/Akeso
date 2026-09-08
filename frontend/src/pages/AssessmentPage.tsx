import { useMutation, useQuery } from "@tanstack/react-query";
import { HelpCircle, ShieldQuestion } from "lucide-react";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { ProgressBar } from "@/components/ui/Progress";
import { ErrorPanel, LoadingPanel } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { iconFor } from "@/features/accessibility/icons";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type {
  AccessibilityNeed,
  AssessmentContent,
  AssessmentPayload,
  AssessmentQuestion,
  AssessmentResult,
} from "@/types/api";

type Answers = Record<string, string | string[]>;

export function AssessmentPage() {
  const { t, s, language } = useI18n();
  const { isEasyMode, isLoading: preferencesLoading } = usePreferences();
  const { advance, isAdvancing } = useAdvance();
  const navigate = useNavigate();

  const [answers, setAnswers] = useState<Answers>({});
  // Easy Mode shows one question per screen; Standard shows them all.
  const [cursor, setCursor] = useState(0);

  const content = useQuery({
    queryKey: ["assessment-content"],
    queryFn: () => api.get<AssessmentContent>("/accessibility/content"),
    staleTime: Infinity,
  });

  const questions = content.data?.questions ?? [];
  const required = useMemo(() => questions.filter((q) => q.required), [questions]);

  const submit = useMutation({
    mutationFn: () => {
      const payload: AssessmentPayload = {
        digital_comfort: answers.digital_comfort as AssessmentPayload["digital_comfort"],
        preferred_interaction: answers.preferred_interaction as AssessmentPayload["preferred_interaction"],
        reading_difficulty: answers.reading_difficulty as AssessmentPayload["reading_difficulty"],
        hearing_difficulty: answers.hearing_difficulty as AssessmentPayload["hearing_difficulty"],
        vision_difficulty: answers.vision_difficulty as AssessmentPayload["vision_difficulty"],
        additional_needs: (answers.additional_needs as AccessibilityNeed[]) ?? [],
      };
      return api.post<AssessmentResult>("/accessibility/assessment", payload);
    },
    onSuccess: (result) => void advance(result.next_route),
  });

  const answerSingle = (field: string, value: string) =>
    setAnswers((current) => ({ ...current, [field]: value }));

  const answerMultiple = (field: string, value: string) =>
    setAnswers((current) => {
      const list = (current[field] as string[] | undefined) ?? [];
      return {
        ...current,
        [field]: list.includes(value) ? list.filter((item) => item !== value) : [...list, value],
      };
    });

  const isAnswered = (question: AssessmentQuestion) => {
    const value = answers[question.field];
    if (question.kind === "multiple") return true; // always optional
    return typeof value === "string" && value.length > 0;
  };

  const answeredCount = required.filter(isAnswered).length;
  const allRequiredAnswered = answeredCount === required.length && required.length > 0;

  // Wait for preferences too: rendering before they arrive would flash the
  // dense standard layout at a patient who asked for Easy Mode.
  if (content.isLoading || preferencesLoading) {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }

  if (content.isError || questions.length === 0) {
    return (
      <AppShell>
        <ErrorPanel
          message={
            content.error instanceof ApiError ? content.error.message : t("errorNetwork")
          }
          onRetry={() => void content.refetch()}
          retryLabel={t("retry")}
        />
      </AppShell>
    );
  }

  const visible = isEasyMode ? questions.slice(cursor, cursor + 1) : questions;
  const currentQuestion = questions[cursor];
  const isLastEasyQuestion = cursor >= questions.length - 1;

  const renderQuestion = (question: AssessmentQuestion) => {
    const value = answers[question.field];
    const multiple = question.kind === "multiple";
    return (
      <fieldset key={question.id} className="space-y-3">
        <legend className="space-y-1">
          <span
            className={
              isEasyMode
                ? "block text-2xl font-semibold leading-snug text-ink"
                : "block text-lg font-semibold text-ink"
            }
          >
            {s(question.prompt)}
            {!question.required && (
              <span className="ml-2 text-base font-normal text-ink-subtle">
                ({t("optional")})
              </span>
            )}
          </span>
          <span className="block text-base text-ink-muted">{s(question.help)}</span>
        </legend>

        <OptionGrid columns={isEasyMode ? 1 : 2}>
          {question.options.map((option) => (
            <OptionCard
              key={option.value}
              name={question.field}
              value={option.value}
              multiple={multiple}
              icon={iconFor(option.icon)}
              label={s(option.label)}
              help={option.help ? s(option.help) : undefined}
              checked={
                multiple
                  ? ((value as string[] | undefined) ?? []).includes(option.value)
                  : value === option.value
              }
              onSelect={(selected) =>
                multiple ? answerMultiple(question.field, selected) : answerSingle(question.field, selected)
              }
            />
          ))}
        </OptionGrid>
      </fieldset>
    );
  };

  return (
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={2}
        title={t("assessmentHeading")}
        description={t("assessmentBody")}
        announce={
          isEasyMode && currentQuestion
            ? `${s(currentQuestion.prompt)}. ${s(currentQuestion.help)}`
            : undefined
        }
        onBack={
          isEasyMode && cursor > 0
            ? () => setCursor((c) => c - 1)
            : () => navigate("/onboarding/personal")
        }
        onNext={
          isEasyMode && !isLastEasyQuestion
            ? () => setCursor((c) => c + 1)
            : () => submit.mutate()
        }
        nextLabel={isEasyMode && !isLastEasyQuestion ? t("continue") : t("continue")}
        nextDisabled={
          isEasyMode
            ? Boolean(currentQuestion && !isAnswered(currentQuestion))
            : !allRequiredAnswered
        }
        isBusy={submit.isPending || isAdvancing}
        footerNote={
          !isEasyMode && !allRequiredAnswered ? t("assessmentSelectToContinue") : undefined
        }
        aside={
          <>
            <Card>
              <CardHeader title={t("assessmentWhyTitle")} icon={<ShieldQuestion className="h-5 w-5" />} />
              <CardBody>
                <p className="text-sm text-ink-muted">{t("assessmentWhyBody")}</p>
              </CardBody>
            </Card>
            <Card>
              <CardBody className="space-y-2">
                <p className="text-sm font-semibold text-ink-muted">
                  {answeredCount} / {required.length} {t("done").toLowerCase()}
                </p>
                <ProgressBar
                  percent={(answeredCount / Math.max(1, required.length)) * 100}
                  label={undefined}
                />
              </CardBody>
            </Card>
          </>
        }
      >
        {isEasyMode && (
          <div className="space-y-2">
            <p className="text-sm font-semibold text-ink-muted">
              {t("assessmentQuestionOf")} {cursor + 1} {t("assessmentOf")} {questions.length}
            </p>
            <ProgressBar percent={((cursor + 1) / questions.length) * 100} />
          </div>
        )}

        {submit.error && (
          <Alert tone="danger">
            {submit.error instanceof ApiError ? submit.error.message : t("errorGeneric")}
          </Alert>
        )}

        <div className={isEasyMode ? "" : "space-y-7"}>{visible.map(renderQuestion)}</div>

        {!isEasyMode && (
          <p className="flex items-start gap-2 text-sm text-ink-subtle">
            <HelpCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            {t("neverLockedNote")}
          </p>
        )}
      </StepLayout>
    </AppShell>
  );
}
