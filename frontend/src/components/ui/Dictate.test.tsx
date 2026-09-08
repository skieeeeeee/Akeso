import { afterEach, describe, expect, it, vi } from "vitest";
import { act, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { renderWithProviders } from "@/test/utils";
import { Dictate } from "@/components/ui/Dictate";
import { STRINGS } from "@/lib/strings";

/**
 * A fake SpeechRecognition, because jsdom has none.
 *
 * `useVoiceInput` reads the constructor off `window` at render, so installing
 * one here exercises the real hook rather than a mock of it — which is the
 * point: the bug being guarded against was the microphone not being rendered
 * at all, and a mocked hook would have hidden it.
 */
class FakeRecognition {
  static latest: FakeRecognition | null = null;
  lang = "";
  continuous = false;
  interimResults = false;
  maxAlternatives = 1;
  onresult: ((event: unknown) => void) | null = null;
  onerror: ((event: { error: string }) => void) | null = null;
  onend: (() => void) | null = null;
  onspeechend: (() => void) | null = null;

  constructor() {
    FakeRecognition.latest = this;
  }

  start() {}
  stop() {
    this.onend?.();
  }
  abort() {}

  /** Deliver a final transcript the way the browser would. */
  say(text: string) {
    this.onresult?.({
      resultIndex: 0,
      results: [Object.assign([{ transcript: text }], { isFinal: true })],
    });
    this.onend?.();
  }
}

function installSpeech() {
  (window as unknown as Record<string, unknown>).SpeechRecognition = FakeRecognition;
}

afterEach(() => {
  delete (window as unknown as Record<string, unknown>).SpeechRecognition;
  FakeRecognition.latest = null;
  vi.restoreAllMocks();
});

describe("Dictate", () => {
  it("offers a microphone when the browser supports speech", () => {
    installSpeech();
    renderWithProviders(<Dictate onText={() => {}} />);
    expect(
      screen.getByRole("button", { name: new RegExp(STRINGS.voiceSpeakInstead.en, "i") }),
    ).toBeTruthy();
  });

  it("renders nothing when the browser cannot do speech", () => {
    // No SpeechRecognition installed: a dead microphone is worse than none.
    const { container } = renderWithProviders(<Dictate onText={() => {}} />);
    expect(container.textContent).toBe("");
  });

  it("hands over what was said", async () => {
    installSpeech();
    const heard = vi.fn();
    renderWithProviders(<Dictate onText={heard} />);

    await userEvent.click(
      screen.getByRole("button", { name: new RegExp(STRINGS.voiceSpeakInstead.en, "i") }),
    );
    expect(screen.getByRole("status").textContent).toContain(STRINGS.voiceListening.en);

    await act(async () => FakeRecognition.latest!.say("penicillin"));
    await waitFor(() => expect(heard).toHaveBeenCalledWith("penicillin"));
  });

  it("hands it over exactly once", async () => {
    // The transcript used to be delivered from render, so any parent re-render
    // appended the same words again.
    installSpeech();
    const heard = vi.fn();
    renderWithProviders(<Dictate onText={heard} />);
    await userEvent.click(
      screen.getByRole("button", { name: new RegExp(STRINGS.voiceSpeakInstead.en, "i") }),
    );
    await act(async () => FakeRecognition.latest!.say("dust allergy"));
    await waitFor(() => expect(heard).toHaveBeenCalledTimes(1));
  });

  it("returns to the microphone afterwards, ready for more", async () => {
    installSpeech();
    renderWithProviders(<Dictate onText={() => {}} />);
    const label = new RegExp(STRINGS.voiceSpeakInstead.en, "i");
    await userEvent.click(screen.getByRole("button", { name: label }));
    await act(async () => FakeRecognition.latest!.say("one"));
    await waitFor(() => expect(screen.getByRole("button", { name: label })).toBeTruthy());
  });

  it("names the field it belongs to, for screen readers", () => {
    installSpeech();
    renderWithProviders(<Dictate onText={() => {}} label="Allergies" />);
    expect(screen.getByRole("button", { name: /Allergies/ })).toBeTruthy();
  });
});
