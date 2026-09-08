import { useCallback, useEffect, useMemo, useState } from "react";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";

/**
 * Audio guidance via the browser's speech synthesiser.
 *
 * Deliberately browser-side: it needs no server, no API key and no network,
 * so it cannot fail in a way that blocks the patient. When synthesis is
 * unavailable `isSupported` is false and the UI simply hides the control —
 * every instruction is always on screen as text as well.
 */

/**
 * BCP-47 locales for speech. All are Indian variants so pronunciation and
 * recognition match how these languages are actually spoken here.
 *
 * Availability varies by platform: en-IN and hi-IN are widely supported,
 * while ta-IN, gu-IN and pa-IN often have no installed voice. The hooks
 * report that rather than failing silently.
 */
const LOCALES: Record<string, string> = {
  en: "en-IN",
  hi: "hi-IN",
  mr: "mr-IN",
  ta: "ta-IN",
  gu: "gu-IN",
  pa: "pa-IN",
};

export function useSpeech() {
  const { language } = useI18n();
  const { preferences } = usePreferences();
  const [isSpeaking, setIsSpeaking] = useState(false);

  const isSupported = useMemo(
    () => typeof window !== "undefined" && "speechSynthesis" in window,
    [],
  );

  // Whether a voice actually exists for the chosen language. Voices load
  // asynchronously, so this is recomputed when the list arrives.
  const [hasVoice, setHasVoice] = useState(true);
  useEffect(() => {
    if (!isSupported) return;
    const check = () => {
      const wanted = (LOCALES[language] ?? "en-IN").slice(0, 2);
      const voices = window.speechSynthesis.getVoices();
      // Before the list populates, assume a voice exists rather than
      // showing a warning that may be wrong.
      setHasVoice(voices.length === 0 || voices.some((v) => v.lang.startsWith(wanted)));
    };
    check();
    window.speechSynthesis.addEventListener?.("voiceschanged", check);
    return () => window.speechSynthesis.removeEventListener?.("voiceschanged", check);
  }, [isSupported, language]);

  const stop = useCallback(() => {
    if (!isSupported) return;
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  }, [isSupported]);

  const speak = useCallback(
    (text: string) => {
      if (!isSupported || !text.trim()) return;
      try {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = LOCALES[language] ?? "en-IN";
        // Slightly slower than default: clearer for first-time users.
        utterance.rate = 0.92;
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);
        window.speechSynthesis.speak(utterance);
        setIsSpeaking(true);
      } catch {
        setIsSpeaking(false);
      }
    },
    [isSupported, language],
  );

  /** Speak only when the patient has audio guidance switched on. */
  const announce = useCallback(
    (text: string) => {
      if (preferences.audio_guidance) speak(text);
    },
    [preferences.audio_guidance, speak],
  );

  // Never leave a sentence playing after the screen changes.
  useEffect(() => stop, [stop]);

  return {
    isSupported,
    /** False when this device has no installed voice for the chosen language. */
    hasVoiceForLanguage: hasVoice,
    isSpeaking,
    speak,
    announce,
    stop,
  };
}
