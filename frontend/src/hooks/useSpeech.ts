import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useI18n } from "@/providers/I18nProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { api, apiBase, authHeaders } from "@/services/apiClient";

/**
 * Audio guidance, from the server when it can and the browser otherwise.
 *
 * The browser's synthesiser needs no key and no network, so it stays the
 * default and the fallback. But a phone or kiosk commonly has *no installed
 * voice* for Marathi, Gujarati or Punjabi, so in those languages it simply
 * cannot speak — which is exactly the patient who most needs a question read
 * aloud. When the server has speech configured it is used instead, which
 * covers every language we ship.
 *
 * Either way audio is an enhancement: every instruction is on screen as text,
 * and any failure falls through to the browser and then to silence, never to
 * a blocked page.
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

  // Whether the server can speak. Asked once; a failure just means "no".
  const serverSpeech = useQuery({
    queryKey: ["speech-status"],
    queryFn: () => api.get<{ available: boolean }>("/speech/status"),
    staleTime: Infinity,
    retry: false,
  });
  const serverCanSpeak = serverSpeech.data?.available === true;

  const audioRef = useRef<HTMLAudioElement | null>(null);
  // True when a request to read something aloud produced no sound at all:
  // the server could not speak and the browser has no voice for this
  // language. The UI says so rather than leaving the patient guessing.
  const [silent, setSilent] = useState(false);

  const stop = useCallback(() => {
    const audio = audioRef.current;
    if (audio) {
      audio.pause();
      if (audio.src.startsWith("blob:")) URL.revokeObjectURL(audio.src);
      audioRef.current = null;
    }
    if (isSupported) window.speechSynthesis.cancel();
    setIsSpeaking(false);
  }, [isSupported]);

  /**
   * Read it with the browser's own voice. The fallback, and the default.
   *
   * @returns false when the browser cannot speak this language at all, so a
   *          caller falling back to it knows the patient heard nothing. Most
   *          devices have no Marathi, Gujarati or Punjabi voice, which meant
   *          every server failure turned into unexplained silence for exactly
   *          the patients who most need the text read aloud.
   */
  const speakLocally = useCallback(
    (text: string): boolean => {
      if (!isSupported || !text.trim()) return false;
      if (!hasVoice) return false;
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
        return true;
      } catch {
        setIsSpeaking(false);
        return false;
      }
    },
    [isSupported, hasVoice, language],
  );

  const speak = useCallback(
    (text: string) => {
      const spoken = text.trim();
      if (!spoken) return;
      setSilent(false);
      if (!serverCanSpeak) {
        if (!speakLocally(spoken)) setSilent(true);
        return;
      }
      stop();
      setIsSpeaking(true);
      void (async () => {
        try {
          const response = await fetch(`${apiBase}/speech`, {
            method: "POST",
            headers: { "Content-Type": "application/json", ...authHeaders() },
            body: JSON.stringify({ text: spoken, language }),
          });
          if (!response.ok) throw new Error(String(response.status));
          const blob = await response.blob();
          const audio = new Audio(URL.createObjectURL(blob));
          audioRef.current = audio;
          audio.onended = () => {
            URL.revokeObjectURL(audio.src);
            setIsSpeaking(false);
          };
          audio.onerror = () => {
            setIsSpeaking(false);
            if (!speakLocally(spoken)) setSilent(true);
          };
          await audio.play();
        } catch {
          // Quota, a concurrency rejection, a network blip: try the browser.
          // If it has no voice for this language the patient hears nothing,
          // and being told that is far better than silence they cannot
          // explain.
          setIsSpeaking(false);
          if (!speakLocally(spoken)) setSilent(true);
        }
      })();
    },
    [serverCanSpeak, speakLocally, stop, language],
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
    // Server speech needs no browser synthesiser, so it counts as support.
    isSupported: isSupported || serverCanSpeak,
    /** A read-aloud was asked for and nothing could say it. */
    silent,
    /**
     * False only when neither the server nor this device can speak the
     * chosen language. Server speech covers all six, so this is true
     * whenever it is configured.
     */
    hasVoiceForLanguage: serverCanSpeak || hasVoice,
    isSpeaking,
    speak,
    announce,
    stop,
  };
}
