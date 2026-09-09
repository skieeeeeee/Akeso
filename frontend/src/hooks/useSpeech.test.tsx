import { afterEach, describe, expect, it, vi } from "vitest";
import { act, cleanup, renderHook, waitFor } from "@testing-library/react";

import { Providers } from "@/test/utils";
import { useSpeech } from "@/hooks/useSpeech";
import { jsonResponse } from "@/test/utils";

/**
 * The failure this guards is silence.
 *
 * When the server cannot speak, the hook falls back to the browser's own
 * voice. Most phones have no Marathi, Gujarati or Punjabi voice, so for three
 * of the six languages that fallback says nothing at all — and it used to say
 * nothing about saying nothing. A patient pressed listen and heard silence,
 * which reads as a broken app rather than a missing voice.
 */

function installSynthesis(voices: string[]) {
  const spoken: string[] = [];
  (window as unknown as Record<string, unknown>).SpeechSynthesisUtterance =
    class {
      lang = "";
      rate = 1;
      onend: (() => void) | null = null;
      onerror: (() => void) | null = null;
      constructor(public text: string) {}
    };
  (window as unknown as Record<string, unknown>).speechSynthesis = {
    getVoices: () => voices.map((lang) => ({ lang, name: lang })),
    speak: (u: { text: string }) => spoken.push(u.text),
    cancel: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
  };
  return spoken;
}

afterEach(() => {
  // Unmount first: the hook's effect cleanup reads window.speechSynthesis,
  // so removing it before React tears down throws.
  cleanup();
  delete (window as unknown as Record<string, unknown>).speechSynthesis;
  delete (window as unknown as Record<string, unknown>).SpeechSynthesisUtterance;
  vi.unstubAllGlobals();
});

const render = (language: string) => {
  window.localStorage.setItem("medikiosk.language", language);
  return renderHook(() => useSpeech(), { wrapper: Providers });
};

describe("reading text aloud", () => {
  it("says so when neither the server nor the device can speak", async () => {
    // No Marathi voice on the device, and the server's speech is off.
    installSynthesis(["en-IN", "hi-IN"]);
    vi.stubGlobal("fetch", () => Promise.resolve(jsonResponse({ available: false })));

    const { result } = render("mr");
    await waitFor(() => expect(result.current.isSupported).toBe(true));

    await act(async () => {
      result.current.speak("आज तुम्हाला काय त्रास होत आहे?");
    });

    await waitFor(() => expect(result.current.silent).toBe(true));
  });

  it("stays quiet about it when the device does have the voice", async () => {
    const spoken = installSynthesis(["en-IN", "hi-IN", "mr-IN"]);
    vi.stubGlobal("fetch", () => Promise.resolve(jsonResponse({ available: false })));

    const { result } = render("mr");
    await waitFor(() => expect(result.current.isSupported).toBe(true));

    await act(async () => {
      result.current.speak("आज तुम्हाला काय त्रास होत आहे?");
    });

    expect(result.current.silent).toBe(false);
    expect(spoken).toHaveLength(1);
  });

  it("reports silence when the server fails and there is no local voice", async () => {
    // This is the real case: ElevenLabs rejects the request — a concurrency
    // limit, a quota — and the fallback has nothing to say it with.
    installSynthesis(["en-IN"]);
    vi.stubGlobal("fetch", (url: string) => {
      if (String(url).includes("/speech/status")) {
        return Promise.resolve(jsonResponse({ available: true }));
      }
      return Promise.resolve(new Response("nope", { status: 503 }));
    });

    const { result } = render("gu");
    await waitFor(() => expect(result.current.isSupported).toBe(true));

    await act(async () => {
      result.current.speak("આજે તમને શું તકલીફ છે?");
    });

    await waitFor(() => expect(result.current.silent).toBe(true));
  });

  it("never flags silence for a language the device can speak", async () => {
    const spoken = installSynthesis(["en-IN"]);
    vi.stubGlobal("fetch", () => Promise.resolve(jsonResponse({ available: false })));

    const { result } = render("en");
    await waitFor(() => expect(result.current.isSupported).toBe(true));

    await act(async () => {
      result.current.speak("What brings you here today?");
    });

    expect(result.current.silent).toBe(false);
    expect(spoken).toEqual(["What brings you here today?"]);
  });
});
