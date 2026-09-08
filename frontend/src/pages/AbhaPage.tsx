import { useMutation, useQuery } from "@tanstack/react-query";
import { BadgeCheck, IdCard, Info } from "lucide-react";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/layout/AppShell";
import { StepLayout } from "@/components/layout/StepLayout";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Field, Input } from "@/components/ui/Field";
import { StatusBadge } from "@/components/ui/Badge";
import { ApiError, api } from "@/services/apiClient";
import { useI18n } from "@/providers/I18nProvider";
import { stepperItems } from "@/features/onboarding/steps";
import { useAdvance } from "@/features/onboarding/useAdvance";
import type { AbhaProfile, AbhaStepResult } from "@/types/api";

export function AbhaPage() {
  const { t, v, language } = useI18n();
  const { advance, isAdvancing } = useAdvance();
  const [abhaId, setAbhaId] = useState("");

  const existing = useQuery({
    queryKey: ["abha"],
    queryFn: () => api.get<AbhaProfile>("/patients/me/abha"),
  });

  // A previous attempt's value is preserved server-side; put it back in the
  // field so the patient never has to retype it.
  useEffect(() => {
    if (existing.data?.abha_id && !abhaId) setAbhaId(existing.data.abha_id);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- prefill once
  }, [existing.data?.abha_id]);

  const link = useMutation({
    mutationFn: () => api.post<AbhaStepResult>("/patients/me/abha/link", { abha_id: abhaId }),
    onSuccess: (result) => void advance(result.next_route),
  });

  const skip = useMutation({
    mutationFn: () => api.post<AbhaStepResult>("/patients/me/abha/skip"),
    onSuccess: (result) => void advance(result.next_route),
  });

  const error = link.error;
  const isUnavailable = error instanceof ApiError && error.status === 503;
  const fieldError =
    error instanceof ApiError && !isUnavailable ? error.message : null;

  return (
    <AppShell>
      <StepLayout
        steps={stepperItems(language)}
        currentIndex={0}
        title={t("abhaHeading")}
        description={t("abhaBody")}
        onNext={() => link.mutate()}
        nextLabel={t("abhaConnect")}
        nextDisabled={abhaId.trim().length < 3}
        isBusy={link.isPending || isAdvancing}
        secondaryAction={
          <Button
            variant="ghost"
            size="md"
            onClick={() => skip.mutate()}
            disabled={skip.isPending || isAdvancing}
          >
            {t("abhaSkip")}
          </Button>
        }
        footerNote={t("progressSavedNote")}
        aside={
          <>
            <Card>
              <CardHeader title={t("abhaWhyTitle")} icon={<Info className="h-5 w-5" />} />
              <CardBody>
                <p className="text-sm text-ink-muted">{t("abhaWhyBody")}</p>
              </CardBody>
            </Card>
            {existing.data && existing.data.verification_status !== "unverified" && (
              <Card>
                <CardBody className="flex items-center justify-between gap-3">
                  <span className="text-sm font-medium text-ink-muted">{t("profileHealthId")}</span>
                  <StatusBadge
                    status={existing.data.verification_status}
                    label={v(existing.data.verification_status)}
                  />
                </CardBody>
              </Card>
            )}
          </>
        }
      >
        {existing.data?.verification_status === "verified" && (
          <Alert tone="success" title={t("abhaConnected")}>
            <p className="font-mono text-lg">{existing.data.abha_id}</p>
          </Alert>
        )}

        {/* The registry being unreachable must never look like a dead end. */}
        {isUnavailable && (
          <Alert
            tone="warning"
            title={t("errorNetwork")}
            action={{ label: t("abhaSkip"), onClick: () => skip.mutate() }}
          >
            <p>{(error as ApiError).message}</p>
          </Alert>
        )}

        <Field
          label={t("abhaLabel")}
          hint={t("abhaHint")}
          error={fieldError}
          required={false}
        >
          {({ inputId, describedBy, invalid }) => (
            <Input
              id={inputId}
              aria-describedby={describedBy}
              aria-invalid={invalid}
              inputMode="text"
              autoComplete="off"
              value={abhaId}
              onChange={(event) => setAbhaId(event.target.value)}
              placeholder="12-3456-7890-1234"
              className="font-mono"
            />
          )}
        </Field>

        {/* Honest about what this integration is. */}
        <Alert tone="info" title={t("prototypeNoticeTitle")}>
          <p className="flex items-start gap-2">
            <IdCard className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
            {t("abhaMockNotice")}
          </p>
        </Alert>

        {skip.error && <Alert tone="danger">{t("errorGeneric")}</Alert>}

        <p className="flex items-center gap-2 text-sm text-ink-subtle">
          <BadgeCheck className="h-4 w-4" aria-hidden="true" />
          {t("neverLockedNote")}
        </p>
      </StepLayout>
    </AppShell>
  );
}
