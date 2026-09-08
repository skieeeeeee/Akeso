import { useEffect, useRef, useState } from "react";
import { Mic, Square } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/States";
import { useVoiceInput } from "@/hooks/useVoiceInput";
import { useI18n } from "@/providers/I18nProvider";

/**
 * A microphone for any single text field.
 *
 * The interview had dictation from the start; nothing else did. So a patient
 * who can speak but struggles to type could describe a symptom in the
 * interview and then be unable to enter their own name, an allergy, or a note
 * about the traditional medicine they take — nine text fields across five
 * pages, all keyboard-only. For the patient this product is aimed at, that is
 * the app quietly closing the door after inviting them in.
 *
 * Deliberately not offered for numeric fields (a date of birth, a phone
 * number, an ABHA id). Dictated digits are the least reliable thing speech
 * recognition returns and the easiest to mistype without noticing, and these
 * are exactly the fields where a wrong value is silent — a keypad is kinder.
 *
 * Renders nothing at all when the browser cannot do speech recognition, so a
 * caller never has to check first. The field stays fully typable throughout:
 * dictation appends to what is already there rather than replacing it.
 */
export function Dictate({
  onText,
  disabled,
  label,
}: {
  /** Called with the finished transcript. Append, never replace. */
  onText: (text: string) => void;
  disabled?: boolean;
  /** Names the field for screen readers, e.g. "Allergies". */
  label?: string;
}) {
  const { t } = useI18n();
  const voice = useVoiceInput();
  const [open, setOpen] = useState(false);

  // `onText` is usually an inline arrow, so it must not be an effect
  // dependency — the effect would re-run on every parent render and hand the
  // same transcript over twice.
  const deliver = useRef(onText);
  deliver.current = onText;

  // Hand the text over as soon as it is final: for a short field there is
  // nothing to confirm that re-reading the field itself does not show.
  useEffect(() => {
    if (voice.state !== "transcript_ready") return;
    const said = voice.transcript.trim();
    voice.reset();
    setOpen(false);
    if (said) deliver.current(said);
  }, [voice.state, voice.transcript, voice.reset]);

  if (!voice.isSupported) return null;

  if (!open) {
    return (
      <Button
        type="button"
        variant="ghost"
        size="md"
        disabled={disabled}
        aria-label={label ? `${t("voiceSpeakInstead")}: ${label}` : undefined}
        onClick={() => {
          setOpen(true);
          voice.start();
        }}
      >
        <Mic className="h-5 w-5" aria-hidden="true" />
        {t("voiceSpeakInstead")}
      </Button>
    );
  }

  if (voice.state === "processing") return <Spinner label={t("voiceProcessing")} />;

  if (voice.state === "failed") {
    return (
      <div className="space-y-2">
        <p role="alert" className="text-sm font-medium text-danger-ink">
          {voice.error ?? t("voiceProblem")}
        </p>
        <Button
          type="button"
          variant="ghost"
          size="md"
          onClick={() => {
            voice.reset();
            setOpen(false);
          }}
        >
          {t("voiceTypeInstead")}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div
        role="status"
        aria-live="polite"
        className="flex items-center gap-2 text-base font-semibold text-primary-ink"
      >
        <span className="relative flex h-3 w-3">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary/60" />
          <span className="relative inline-flex h-3 w-3 rounded-full bg-primary" />
        </span>
        {t("voiceListening")}
      </div>
      {voice.interim && <p className="text-sm italic text-ink-muted">{voice.interim}</p>}
      <Button
        type="button"
        variant="secondary"
        size="md"
        onClick={() => {
          voice.stop();
        }}
      >
        <Square className="h-4 w-4" aria-hidden="true" />
        {t("voiceStop")}
      </Button>
    </div>
  );
}
