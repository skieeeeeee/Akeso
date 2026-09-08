import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useI18n } from "@/providers/I18nProvider";

/**
 * Speech-to-text for answering questions.
 *
 * Uses the browser's SpeechRecognition, so there is no server dependency and
 * nothing to fail on the backend. The important property is that voice is
 * never mandatory: `isSupported` is false when the browser cannot do it, every
 * failure produces an actionable message, and the caller always renders a
 * typing fallback alongside the microphone.
 *
 * The state machine is explicit so the UI can explain what is happening
 * rather than showing an unlabelled spinner:
 *   idle -> listening -> processing -> transcript_ready | failed
 */

export type VoiceState =
  | "idle"
  | "listening"
  | "processing"
  | "transcript_ready"
  | "failed";

type RecognitionAlternative = { transcript: string };
type RecognitionResult = ArrayLike<RecognitionAlternative> & { isFinal: boolean };
type RecognitionEvent = {
  results: ArrayLike<RecognitionResult>;
  resultIndex: number;
};

type Recognition = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  start: () => void;
  stop: () => void;
  abort: () => void;
  onresult: ((event: RecognitionEvent) => void) | null;
  onerror: ((event: { error: string }) => void) | null;
  onend: (() => void) | null;
  onspeechend: (() => void) | null;
};

type RecognitionCtor = new () => Recognition;

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

/** Every failure the API can report, mapped to something a patient can act on. */
const ERRORS: Record<string, { en: string; hi: string }> = {
  "not-allowed": {
    en: "Microphone permission was denied. You can type your answer instead.",
    hi: "माइक्रोफ़ोन की अनुमति नहीं मिली। आप अपना जवाब टाइप कर सकते हैं।",
  },
  "service-not-allowed": {
    en: "Voice input is blocked in this browser. Please type your answer.",
    hi: "इस ब्राउज़र में आवाज़ इनपुट बंद है। कृपया अपना जवाब टाइप करें।",
  },
  "no-speech": {
    en: "I did not hear anything. Try again, or type your answer.",
    hi: "मुझे कुछ सुनाई नहीं दिया। फिर कोशिश करें, या टाइप करें।",
  },
  "audio-capture": {
    en: "No microphone was found. Please type your answer.",
    hi: "कोई माइक्रोफ़ोन नहीं मिला। कृपया अपना जवाब टाइप करें।",
  },
  network: {
    en: "Voice input needs a network connection. Please type your answer.",
    hi: "आवाज़ इनपुट के लिए नेटवर्क चाहिए। कृपया अपना जवाब टाइप करें।",
  },
  aborted: { en: "", hi: "" },
};

function recognitionCtor(): RecognitionCtor | null {
  if (typeof window === "undefined") return null;
  const scope = window as unknown as {
    SpeechRecognition?: RecognitionCtor;
    webkitSpeechRecognition?: RecognitionCtor;
  };
  return scope.SpeechRecognition ?? scope.webkitSpeechRecognition ?? null;
}

export function useVoiceInput() {
  const { language } = useI18n();
  const ctor = useMemo(recognitionCtor, []);
  const recognition = useRef<Recognition | null>(null);
  const finalRef = useRef("");

  const [state, setState] = useState<VoiceState>("idle");
  const [transcript, setTranscript] = useState("");
  const [interim, setInterim] = useState("");
  const [error, setError] = useState<string | null>(null);

  const reset = useCallback(() => {
    recognition.current?.abort();
    recognition.current = null;
    finalRef.current = "";
    setState("idle");
    setTranscript("");
    setInterim("");
    setError(null);
  }, []);

  const stop = useCallback(() => {
    // Stop, don't abort: a graceful stop still delivers the final result.
    recognition.current?.stop();
    setState((current) => (current === "listening" ? "processing" : current));
  }, []);

  const start = useCallback(() => {
    if (!ctor) return;
    finalRef.current = "";
    setTranscript("");
    setInterim("");
    setError(null);

    const instance = new ctor();
    instance.lang = LOCALES[language] ?? "en-IN";
    instance.continuous = false;
    instance.interimResults = true;
    instance.maxAlternatives = 1;

    instance.onresult = (event) => {
      let live = "";
      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        const result = event.results[index];
        if (!result) continue;
        const text = result[0]?.transcript ?? "";
        if (result.isFinal) finalRef.current += text;
        else live += text;
      }
      setInterim(live.trim());
      if (finalRef.current.trim()) setTranscript(finalRef.current.trim());
    };

    instance.onerror = (event) => {
      const message = (ERRORS[event.error] ?? {
        en: "Voice input failed. Please type your answer.",
        hi: "आवाज़ इनपुट विफल रहा। कृपया अपना जवाब टाइप करें।",
      })[language === "hi" ? "hi" : "en"];
      if (message) {
        setError(message);
        setState("failed");
      } else {
        setState("idle");
      }
    };

    // Give the engine a moment to deliver its final result before judging.
    instance.onspeechend = () => setState("processing");
    instance.onend = () => {
      setInterim("");
      setState((current) => {
        if (current === "failed") return current;
        const heard = finalRef.current.trim();
        if (heard) {
          setTranscript(heard);
          return "transcript_ready";
        }
        setError(ERRORS["no-speech"]![language === "hi" ? "hi" : "en"]);
        return "failed";
      });
    };

    recognition.current = instance;
    try {
      instance.start();
      setState("listening");
    } catch {
      setError(
        language === "hi"
          ? "आवाज़ इनपुट शुरू नहीं हो सका। कृपया टाइप करें।"
          : "Voice input could not start. Please type your answer.",
      );
      setState("failed");
    }
  }, [ctor, language]);

  /**
   * Let the patient correct what was heard before confirming.
   *
   * Stays in `transcript_ready` even when the box is momentarily empty —
   * clearing it to retype must not tear the review panel down mid-edit. The
   * confirm button handles emptiness by staying disabled.
   */
  const editTranscript = useCallback((next: string) => {
    finalRef.current = next;
    setTranscript(next);
    setState("transcript_ready");
  }, []);

  // Never leave the microphone open when the screen changes.
  useEffect(
    () => () => {
      recognition.current?.abort();
    },
    [],
  );

  return {
    isSupported: ctor !== null,
    state,
    isListening: state === "listening",
    transcript,
    interim,
    error,
    start,
    stop,
    reset,
    editTranscript,
  };
}
