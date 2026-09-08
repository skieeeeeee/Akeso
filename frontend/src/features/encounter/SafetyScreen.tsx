import { PhoneCall, ShieldAlert, TriangleAlert } from "lucide-react";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { Spinner } from "@/components/ui/States";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import type { RedFlagState } from "@/types/api";

/**
 * The emergency safety screen.
 *
 * Two deliberate properties:
 *
 * 1. Nothing here names a condition. The wording comes from the server and
 *    says "may require urgent medical attention" plus an explicit "this does
 *    not confirm a medical condition".
 * 2. Neither action clears the flag. "Continue answering" only acknowledges
 *    that the patient has read this, so triggering the emergency path is
 *    never a way to skip the interview.
 */
export function SafetyScreen({
  safety,
  onRequestAssistance,
  onContinue,
  isBusy,
  assistanceSent,
}: {
  safety: RedFlagState;
  onRequestAssistance: () => void;
  onContinue: () => void;
  isBusy?: boolean;
  assistanceSent?: boolean;
}) {
  const { t, s } = useI18n();
  const { isEasyMode } = usePreferences();
  const notice = safety.notice;
  if (!notice) return null;

  return (
    <div className="space-y-4">
      <Card className="border-danger/40 bg-danger-soft">
        <CardBody className="space-y-5 py-7">
          <div className="flex items-start gap-4">
            <span
              aria-hidden="true"
              className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-danger text-white"
            >
              <ShieldAlert className="h-8 w-8" />
            </span>
            {/* The wrapper carries role="alert" so this is announced
                immediately; putting it on the <h1> would override the
                heading role and remove it from the document outline. */}
            <div className="min-w-0 space-y-2" role="alert">
              <h1
                className={
                  isEasyMode
                    ? "text-3xl font-bold leading-snug text-danger-ink"
                    : "text-2xl font-bold leading-snug text-danger-ink"
                }
              >
                {s(notice.title)}
              </h1>
              <p className={isEasyMode ? "text-xl text-danger-ink" : "text-lg text-danger-ink"}>
                {s(notice.body)}
              </p>
            </div>
          </div>

          {/* Says plainly that this is not a diagnosis. */}
          <Alert tone="warning">{s(notice.disclaimer)}</Alert>

          <p className="text-lg font-semibold text-danger-ink">{s(notice.instruction)}</p>

          {assistanceSent && <Alert tone="success">{t("urgentAssistanceSent")}</Alert>}

          <div className="flex flex-col gap-3 sm:flex-row">
            <Button
              size={isEasyMode ? "xl" : "lg"}
              variant="danger"
              onClick={onRequestAssistance}
              disabled={isBusy}
              className="flex-1"
            >
              {isBusy ? (
                <Spinner className="text-white" />
              ) : (
                <>
                  <PhoneCall className="h-6 w-6" aria-hidden="true" />
                  {s(notice.action_staff)}
                </>
              )}
            </Button>
            <Button
              size={isEasyMode ? "xl" : "lg"}
              variant="secondary"
              onClick={onContinue}
              disabled={isBusy}
              className="flex-1"
            >
              {s(notice.action_continue)}
            </Button>
          </div>

          {/* Stated up front: the patient cannot switch this off. */}
          <p className="text-sm text-danger-ink/90">{t("urgentCannotRemove")}</p>
        </CardBody>
      </Card>

      {safety.flags.length > 0 && (
        <Card>
          <CardBody className="space-y-2">
            <p className="text-sm font-semibold text-ink-muted">{t("urgentWhy")}</p>
            <ul className="space-y-1">
              {safety.flags.map((flag) => (
                <li key={`${flag.category}-${flag.created_at}`} className="text-base text-ink">
                  “{flag.evidence}”
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
      )}
    </div>
  );
}

/** Persistent banner shown on every screen while a flag is active. */
export function UrgentBanner() {
  const { t } = useI18n();
  return (
    <div
      role="status"
      className="flex items-center gap-3 rounded-2xl border-2 border-danger/40 bg-danger-soft px-4 py-3"
    >
      <TriangleAlert className="h-5 w-5 shrink-0 text-danger" aria-hidden="true" />
      {/* The banner is the indicator; a badge here would just repeat its
          own opening words. */}
      <p className="text-base font-semibold text-danger-ink">{t("urgentBanner")}</p>
    </div>
  );
}
