import { Check, Keyboard, Mic, MicOff, Pencil, Plus, Square, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Input, Textarea } from "@/components/ui/Field";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { Spinner } from "@/components/ui/States";
import { cn } from "@/lib/cn";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { useVoiceInput } from "@/hooks/useVoiceInput";
import { iconFor } from "@/features/accessibility/icons";
import type { InputMethod, InterviewQuestion } from "@/types/api";

/**
 * The one place an answer is composed, whatever the input method.
 *
 * It hands the caller a plain string plus the method used, which is exactly
 * what the API takes — so voice, touch and typing converge before anything
 * clinical sees them. Voice is offered when the browser supports it and the
 * patient asked for it, and typing is *always* available underneath.
 */

export type AnswerDraft = { text: string; method: InputMethod };

export function AnswerInput({
  question,
  onSubmit,
  disabled,
}: {
  question: InterviewQuestion;
  onSubmit: (draft: AnswerDraft) => void;
  disabled?: boolean;
}) {
  const { t, language } = useI18n();
  const { preferences, isEasyMode } = usePreferences();
  const voice = useVoiceInput();

  const [typed, setTyped] = useState("");
  const [items, setItems] = useState<string[]>([]);
  const [chosen, setChosen] = useState<string[]>([]);
  const [showTyping, setShowTyping] = useState(false);

  // A new question means a clean slate.
  useEffect(() => {
    setTyped("");
    setItems([]);
    setChosen([]);
    setShowTyping(false);
    voice.reset();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- reset per question
  }, [question.instance_key]);

  const wantsVoice =
    voice.isSupported && preferences.interaction_preference !== "touch";

  const isChoice =
    question.kind === "single_choice" ||
    question.kind === "yes_no" ||
    question.kind === "scale";
  const isMulti = question.kind === "multi_choice";
  const isList = question.kind === "list";

  // --- choice questions: one tap answers -------------------------------
  if (isChoice) {
    return (
      <div className="space-y-4">
        <OptionGrid columns={question.kind === "scale" ? 3 : isEasyMode ? 1 : 2}>
          {question.options.map((option) => (
            <OptionCard
              key={option.value}
              name={question.instance_key}
              value={option.value}
              checked={false}
              icon={iconFor(option.icon ?? undefined)}
              label={option.label}
              onSelect={(value) => onSubmit({ text: value, method: "touch" })}
            />
          ))}
        </OptionGrid>
        {question.allow_none && !question.required && (
          <Button
            variant="ghost"
            size="md"
            disabled={disabled}
            onClick={() => onSubmit({ text: "no", method: "touch" })}
          >
            {t("medicalNothingToAdd")}
          </Button>
        )}
      </div>
    );
  }

  // --- multi-choice: pick several, then continue ------------------------
  if (isMulti) {
    const toggle = (value: string) =>
      setChosen((current) =>
        current.includes(value)
          ? current.filter((entry) => entry !== value)
          : [...current, value],
      );
    return (
      <div className="space-y-4">
        <OptionGrid columns={isEasyMode ? 1 : 2}>
          {question.options.map((option) => (
            <OptionCard
              key={option.value}
              name={question.instance_key}
              value={option.value}
              multiple
              checked={chosen.includes(option.value)}
              icon={iconFor(option.icon ?? undefined)}
              label={option.label}
              onSelect={toggle}
            />
          ))}
        </OptionGrid>
        <div className="flex flex-wrap gap-2">
          <Button
            disabled={disabled || chosen.length === 0}
            onClick={() => onSubmit({ text: chosen.join(", "), method: "touch" })}
          >
            {t("continue")}
          </Button>
          <Button
            variant="ghost"
            disabled={disabled}
            onClick={() => onSubmit({ text: "no", method: "touch" })}
          >
            {t("medicalNothingToAdd")}
          </Button>
        </div>
      </div>
    );
  }

  // --- free text and list: voice, typing, and quick picks --------------
  const addItem = (value: string) => {
    const cleaned = value.trim().replace(/\s+/g, " ");
    if (!cleaned) return;
    setItems((current) =>
      current.some((entry) => entry.toLowerCase() === cleaned.toLowerCase())
        ? current
        : [...current, cleaned],
    );
    setTyped("");
    voice.reset();
  };

  const submitFreeText = (method: InputMethod, text: string) => {
    const value = text.trim();
    if (!value) return;
    onSubmit({ text: value, method });
  };

  const submitList = (method: InputMethod) => {
    const all = [...items, typed.trim(), voice.transcript.trim()].filter(Boolean);
    if (all.length === 0) return;
    onSubmit({ text: all.join(", "), method });
  };

  return (
    <div className="space-y-4">
      {/* Quick picks: essential for low-literacy and Easy Mode patients. */}
      {question.suggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-semibold text-ink-subtle">{t("medicalQuickAdd")}</p>
          <div className="flex flex-wrap gap-2">
            {question.suggestions.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                disabled={disabled}
                onClick={() =>
                  isList ? addItem(suggestion) : onSubmit({ text: suggestion, method: "touch" })
                }
                className="min-h-[2.75rem] rounded-full border-2 border-line bg-surface px-4 py-2 text-base font-medium text-ink transition-colors hover:border-primary hover:bg-primary-soft disabled:opacity-45"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Items already added for a list question. */}
      {isList && items.length > 0 && (
        <ul className="flex flex-wrap gap-2">
          {items.map((item) => (
            <li key={item}>
              <span className="inline-flex items-center gap-2 rounded-full border-2 border-primary/30 bg-primary-soft px-3 py-1.5 text-base font-medium text-primary-ink">
                {item}
                <button
                  type="button"
                  aria-label={`${t("remove")}: ${item}`}
                  onClick={() => setItems((c) => c.filter((entry) => entry !== item))}
                  className="rounded-full p-0.5 hover:bg-primary/15"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}

      {/* --- Voice ------------------------------------------------------ */}
      {wantsVoice && (
        <div className="space-y-3 rounded-2xl border-2 border-line bg-surface-muted p-4">
          {voice.state === "idle" && (
            <Button size={isEasyMode ? "xl" : "lg"} block disabled={disabled} onClick={voice.start}>
              <Mic className="h-6 w-6" aria-hidden="true" />
              {t("voiceTapToSpeak")}
            </Button>
          )}

          {voice.state === "listening" && (
            <div className="space-y-3">
              <div
                role="status"
                aria-live="polite"
                className="flex items-center gap-3 text-lg font-semibold text-primary-ink"
              >
                <span className="relative flex h-4 w-4">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary/60" />
                  <span className="relative inline-flex h-4 w-4 rounded-full bg-primary" />
                </span>
                {t("voiceListening")}
              </div>
              {voice.interim && <p className="text-base italic text-ink-muted">{voice.interim}</p>}
              <Button variant="secondary" size="lg" block onClick={voice.stop}>
                <Square className="h-5 w-5" aria-hidden="true" />
                {t("voiceStop")}
              </Button>
            </div>
          )}

          {voice.state === "processing" && <Spinner label={t("voiceProcessing")} />}

          {/* The patient reviews and may correct the transcription. */}
          {voice.state === "transcript_ready" && (
            <div className="space-y-3">
              <p className="text-sm font-semibold text-ink-subtle">{t("voiceHeard")}</p>
              <Textarea
                aria-label={t("voiceHeard")}
                rows={2}
                value={voice.transcript}
                onChange={(event) => voice.editTranscript(event.target.value)}
              />
              <div className="flex flex-wrap gap-2">
                <Button
                  disabled={disabled || !voice.transcript.trim()}
                  onClick={() =>
                    isList ? addItem(voice.transcript) : submitFreeText("voice", voice.transcript)
                  }
                >
                  <Check className="h-5 w-5" aria-hidden="true" />
                  {isList ? t("add") : t("voiceConfirm")}
                </Button>
                <Button variant="secondary" onClick={voice.start} disabled={disabled}>
                  <Mic className="h-5 w-5" aria-hidden="true" />
                  {t("voiceAgain")}
                </Button>
                <Button variant="ghost" onClick={() => setShowTyping(true)}>
                  <Pencil className="h-5 w-5" aria-hidden="true" />
                  {t("voiceTypeInstead")}
                </Button>
              </div>
            </div>
          )}

          {/* A voice failure never blocks the answer. */}
          {voice.state === "failed" && voice.error && (
            <Alert tone="warning" title={t("voiceProblem")}>
              <p>{voice.error}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <Button variant="secondary" size="md" onClick={voice.start}>
                  <Mic className="h-5 w-5" aria-hidden="true" />
                  {t("retry")}
                </Button>
                <Button variant="secondary" size="md" onClick={() => setShowTyping(true)}>
                  <Keyboard className="h-5 w-5" aria-hidden="true" />
                  {t("voiceTypeInstead")}
                </Button>
              </div>
            </Alert>
          )}
        </div>
      )}

      {/* --- Typing (always reachable) ---------------------------------- */}
      {(!wantsVoice || showTyping || voice.state === "idle" || items.length > 0) && (
        <form
          className="space-y-3"
          onSubmit={(event) => {
            event.preventDefault();
            if (isList) {
              if (typed.trim()) addItem(typed);
              else submitList("text");
            } else {
              submitFreeText("text", typed);
            }
          }}
        >
          <div className={cn("flex gap-2", isEasyMode && "flex-col")}>
            <Input
              aria-label={question.text}
              placeholder={t("medicalAddPlaceholder")}
              value={typed}
              disabled={disabled}
              onChange={(event) => setTyped(event.target.value)}
            />
            <Button type="submit" variant="secondary" disabled={disabled || !typed.trim()}>
              {isList ? (
                <>
                  <Plus className="h-5 w-5" aria-hidden="true" />
                  {t("add")}
                </>
              ) : (
                t("continue")
              )}
            </Button>
          </div>
        </form>
      )}

      {/* --- Submit / skip --------------------------------------------- */}
      <div className="flex flex-wrap gap-2">
        {isList && (items.length > 0 || typed.trim()) && (
          <Button disabled={disabled} onClick={() => submitList("text")}>
            {t("continue")}
          </Button>
        )}
        {question.allow_none && !question.required && (
          <Button
            variant="ghost"
            disabled={disabled}
            onClick={() => onSubmit({ text: "no", method: "touch" })}
          >
            <MicOff className="h-5 w-5" aria-hidden="true" />
            {t("medicalNothingToAdd")}
          </Button>
        )}
      </div>

      {!voice.isSupported && preferences.interaction_preference !== "touch" && (
        <p className="text-sm text-ink-subtle">{t("voiceUnavailable")}</p>
      )}
      <span className="sr-only">{language}</span>
    </div>
  );
}
