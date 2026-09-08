import { ArrowLeft, ArrowRight, Volume2, VolumeX } from "lucide-react";
import { useEffect, type ReactNode } from "react";
import { cn } from "@/lib/cn";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardFooter } from "@/components/ui/Card";
import { Stepper, type StepperItem } from "@/components/ui/Progress";
import { Spinner } from "@/components/ui/States";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { useSpeech } from "@/hooks/useSpeech";

/**
 * The single layout every onboarding step uses.
 *
 * Easy Mode is a presentation change here — larger type, more spacing, a
 * single visible action — rather than a separate set of screens. The step
 * content itself is identical in both modes.
 */
export function StepLayout({
  steps,
  currentIndex,
  title,
  description,
  children,
  aside,
  onBack,
  onNext,
  nextLabel,
  nextDisabled,
  isBusy,
  secondaryAction,
  footerNote,
  announce,
}: {
  steps: StepperItem[];
  currentIndex: number;
  title: string;
  description?: string;
  children: ReactNode;
  aside?: ReactNode;
  onBack?: () => void;
  onNext?: () => void;
  nextLabel?: string;
  nextDisabled?: boolean;
  isBusy?: boolean;
  secondaryAction?: ReactNode;
  footerNote?: ReactNode;
  /** Text read aloud when audio guidance is on. Defaults to title + description. */
  announce?: string;
}) {
  const { t } = useI18n();
  const { isEasyMode, preferences } = usePreferences();
  const speech = useSpeech();

  const spoken = announce ?? [title, description].filter(Boolean).join(". ");

  // Read the step aloud when the patient asked for audio guidance.
  useEffect(() => {
    if (!preferences.audio_guidance) return;
    speech.announce(spoken);
    return speech.stop;
    // eslint-disable-next-line react-hooks/exhaustive-deps -- re-announce per step
  }, [spoken, preferences.audio_guidance]);

  return (
    <div className="space-y-5">
      <Stepper steps={steps} currentIndex={currentIndex} />

      <div className={cn("grid gap-5", aside && !isEasyMode && "lg:grid-cols-[1fr_18rem]")}>
        <Card>
          <div className="border-b border-line px-5 py-5 sm:px-6">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h1
                  className={cn(
                    "font-bold leading-tight text-ink",
                    isEasyMode ? "text-3xl" : "text-2xl",
                  )}
                >
                  {title}
                </h1>
                {description && (
                  <p className={cn("mt-2 text-ink-muted", isEasyMode ? "text-lg" : "text-base")}>
                    {description}
                  </p>
                )}
              </div>

              {speech.isSupported && speech.hasVoiceForLanguage && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => (speech.isSpeaking ? speech.stop() : speech.speak(spoken))}
                  aria-label={speech.isSpeaking ? t("consentStopListening") : t("consentListen")}
                  title={speech.isSpeaking ? t("consentStopListening") : t("consentListen")}
                >
                  {speech.isSpeaking ? (
                    <VolumeX className="h-5 w-5" aria-hidden="true" />
                  ) : (
                    <Volume2 className="h-5 w-5" aria-hidden="true" />
                  )}
                </Button>
              )}
            </div>
          </div>

          <CardBody className={isEasyMode ? "space-y-6 py-7" : "space-y-5"}>{children}</CardBody>

          {(onBack || onNext || secondaryAction || footerNote) && (
            <CardFooter>
              <div className="flex items-center gap-2">
                {onBack && (
                  <Button variant="ghost" size={isEasyMode ? "lg" : "md"} onClick={onBack}>
                    <ArrowLeft className="h-5 w-5" aria-hidden="true" />
                    {t("back")}
                  </Button>
                )}
                {secondaryAction}
              </div>

              <div className="flex flex-col items-stretch gap-2 sm:flex-row sm:items-center">
                {footerNote && (
                  <p className="order-2 text-sm text-ink-subtle sm:order-1 sm:mr-2">{footerNote}</p>
                )}
                {onNext && (
                  <Button
                    size={isEasyMode ? "xl" : "lg"}
                    onClick={onNext}
                    disabled={nextDisabled || isBusy}
                    className="order-1 sm:order-2"
                  >
                    {isBusy ? (
                      <Spinner label={t("saving")} className="text-white" />
                    ) : (
                      <>
                        {nextLabel ?? t("continue")}
                        <ArrowRight className="h-5 w-5" aria-hidden="true" />
                      </>
                    )}
                  </Button>
                )}
              </div>
            </CardFooter>
          )}
        </Card>

        {/* Supporting context. Hidden in Easy Mode to keep one task per screen. */}
        {aside && !isEasyMode && <div className="space-y-4">{aside}</div>}
      </div>
    </div>
  );
}
