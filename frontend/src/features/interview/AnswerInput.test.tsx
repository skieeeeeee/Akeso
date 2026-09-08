import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AnswerInput } from "./AnswerInput";
import { PREFERENCES, question } from "@/test/fixtures";
import { SESSION, jsonResponse, renderWithProviders, route, signInForTest, stubFetch } from "@/test/utils";

/** A controllable stand-in for the browser's SpeechRecognition. */
class FakeRecognition {
  static last: FakeRecognition | null = null;
  lang = "";
  continuous = false;
  interimResults = false;
  maxAlternatives = 1;
  onresult: ((event: unknown) => void) | null = null;
  onerror: ((event: { error: string }) => void) | null = null;
  onend: (() => void) | null = null;
  onspeechend: (() => void) | null = null;
  started = false;

  constructor() {
    FakeRecognition.last = this;
  }
  start() {
    this.started = true;
  }
  stop() {}
  abort() {}

  /** Simulate the engine returning a final transcript. */
  finish(transcript: string) {
    this.onresult?.({
      resultIndex: 0,
      results: [Object.assign([{ transcript }], { isFinal: true })],
    });
    this.onend?.();
  }
  fail(error: string) {
    this.onerror?.({ error });
    this.onend?.();
  }
}

function stubPreferences(preferences = PREFERENCES) {
  stubFetch([
    route("/auth/me", () => jsonResponse(SESSION)),
    route("/accessibility/preferences", () => jsonResponse(preferences)),
  ]);
}

beforeEach(() => {
  signInForTest();
  FakeRecognition.last = null;
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("AnswerInput — typing always works", () => {
  it("typing is available even with no speech support", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences();
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    // jsdom has no SpeechRecognition, so this is the no-voice case.
    expect(screen.queryByRole("button", { name: /tap to speak/i })).not.toBeInTheDocument();

    await user.type(screen.getByLabelText(/what problem brings you in/i), "Headache");
    await user.click(screen.getByRole("button", { name: /continue/i }));

    expect(onSubmit).toHaveBeenCalledWith({ text: "Headache", method: "text" });
  });

  it("explains when voice is unavailable but was preferred", async () => {
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);
    expect(await screen.findByText(/voice input is not available/i)).toBeInTheDocument();
  });

  it("a quick pick submits as touch", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences();
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    await user.click(screen.getByRole("button", { name: "Fever" }));
    expect(onSubmit).toHaveBeenCalledWith({ text: "Fever", method: "touch" });
  });

  it("a list question collects several items before submitting", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences();
    renderWithProviders(
      <AnswerInput
        question={question({ kind: "list", suggestions: [], text: "Which medicines?" })}
        onSubmit={onSubmit}
      />,
    );

    const field = screen.getByLabelText("Which medicines?");
    await user.type(field, "Metformin");
    await user.click(screen.getByRole("button", { name: /^add$/i }));
    await user.type(field, "Aspirin");
    await user.click(screen.getByRole("button", { name: /^add$/i }));

    expect(screen.getByText("Metformin")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /^continue$/i }));
    expect(onSubmit).toHaveBeenCalledWith({ text: "Metformin, Aspirin", method: "text" });
  });

  it("an item can be removed before submitting", async () => {
    const user = userEvent.setup();
    stubPreferences();
    renderWithProviders(
      <AnswerInput question={question({ kind: "list", suggestions: [] })} onSubmit={vi.fn()} />,
    );

    await user.type(screen.getByLabelText(/what problem/i), "Metformin");
    await user.click(screen.getByRole("button", { name: /^add$/i }));
    await user.click(screen.getByRole("button", { name: /remove: metformin/i }));
    expect(screen.queryByText("Metformin")).not.toBeInTheDocument();
  });

  it("a multi-choice question submits the chosen values", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences();
    renderWithProviders(
      <AnswerInput
        question={question({
          kind: "multi_choice",
          suggestions: [],
          options: [
            { value: "Fever", label: "Fever", icon: null },
            { value: "Cough", label: "Cough", icon: null },
          ],
        })}
        onSubmit={onSubmit}
      />,
    );

    await user.click(screen.getByRole("checkbox", { name: "Fever" }));
    await user.click(screen.getByRole("checkbox", { name: "Cough" }));
    await user.click(screen.getByRole("button", { name: /^continue$/i }));
    expect(onSubmit).toHaveBeenCalledWith({ text: "Fever, Cough", method: "touch" });
  });

  it("an optional question can be answered with nothing", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences();
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    await user.click(screen.getByRole("button", { name: /nothing to add/i }));
    expect(onSubmit).toHaveBeenCalledWith({ text: "no", method: "touch" });
  });

  it("a required question offers no skip", async () => {
    stubPreferences();
    renderWithProviders(
      <AnswerInput question={question({ required: true, allow_none: false })} onSubmit={vi.fn()} />,
    );
    expect(screen.queryByRole("button", { name: /nothing to add/i })).not.toBeInTheDocument();
  });
});

describe("AnswerInput — voice", () => {
  beforeEach(() => {
    vi.stubGlobal("SpeechRecognition", FakeRecognition);
  });

  it("shows a listening state, then the transcript for review", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences({ ...PREFERENCES, interaction_preference: "hybrid" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    expect(screen.getByText(/listening/i)).toBeInTheDocument();

    FakeRecognition.last!.finish("Chest pain since three days");

    // The patient reviews (and may edit) before it is accepted.
    expect(await screen.findByDisplayValue("Chest pain since three days")).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();

    await user.click(screen.getByRole("button", { name: /that is right/i }));
    expect(onSubmit).toHaveBeenCalledWith({
      text: "Chest pain since three days",
      method: "voice",
    });
  });

  it("the transcript can be corrected before confirming", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.finish("chest pane");

    const box = await screen.findByDisplayValue("chest pane");
    await user.clear(box);
    await user.type(box, "chest pain");
    await user.click(screen.getByRole("button", { name: /that is right/i }));

    expect(onSubmit).toHaveBeenCalledWith({ text: "chest pain", method: "voice" });
  });

  it("a denied microphone offers typing instead", async () => {
    const user = userEvent.setup();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.fail("not-allowed");

    expect(await screen.findByText(/microphone permission was denied/i)).toBeInTheDocument();
    // Both escapes are offered — the patient is never trapped.
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /type instead/i })).toBeInTheDocument();
  });

  it("silence is reported and retryable", async () => {
    const user = userEvent.setup();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.fail("no-speech");

    expect(await screen.findByText(/did not hear anything/i)).toBeInTheDocument();
  });

  it("an empty result is treated as silence, not success", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={onSubmit} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.onend?.();

    expect(await screen.findByText(/did not hear anything/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("a network failure points at typing", async () => {
    const user = userEvent.setup();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.fail("network");

    expect(await screen.findByText(/needs a network connection/i)).toBeInTheDocument();
  });

  it("voice is not offered to a touch-only patient", async () => {
    stubPreferences({ ...PREFERENCES, interaction_preference: "touch" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);
    await waitFor(() =>
      expect(screen.queryByRole("button", { name: /tap to speak/i })).not.toBeInTheDocument(),
    );
  });

  it("a spoken item can be added to a list", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(
      <AnswerInput question={question({ kind: "list", suggestions: [] })} onSubmit={onSubmit} />,
    );

    await user.click(await screen.findByRole("button", { name: /tap to speak/i }));
    FakeRecognition.last!.finish("Metformin");
    await user.click(await screen.findByRole("button", { name: /^add$/i }));

    expect(screen.getByText("Metformin")).toBeInTheDocument();
  });
});

describe("dictation is available whatever the interaction preference", () => {
  it("a touch-preferring patient can still reach the microphone", async () => {
    // `interaction_preference: "touch"` used to remove dictation entirely —
    // including from the demo patient most people open first, so the headline
    // feature looked missing. It decides prominence now, not availability.
    const user = userEvent.setup();
    vi.stubGlobal("SpeechRecognition", FakeRecognition);
    stubPreferences({ ...PREFERENCES, interaction_preference: "touch" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);

    const open = await screen.findByRole("button", { name: /speak instead/i });
    await user.click(open);
    expect(await screen.findByRole("button", { name: /tap to speak/i })).toBeInTheDocument();
  });

  it("a voice-preferring patient gets the microphone straight away", async () => {
    vi.stubGlobal("SpeechRecognition", FakeRecognition);
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(<AnswerInput question={question()} onSubmit={vi.fn()} />);

    expect(await screen.findByRole("button", { name: /tap to speak/i })).toBeInTheDocument();
    // No extra step to get there.
    expect(screen.queryByRole("button", { name: /speak instead/i })).not.toBeInTheDocument();
  });

  it("tapping questions still have no microphone", async () => {
    // Dictating a choice adds nothing, so those stay tap-only.
    vi.stubGlobal("SpeechRecognition", FakeRecognition);
    stubPreferences({ ...PREFERENCES, interaction_preference: "voice" });
    renderWithProviders(
      <AnswerInput
        question={question({
          kind: "single_choice",
          options: [{ value: "yes", label: "Yes", icon: null }],
        })}
        onSubmit={vi.fn()}
      />,
    );
    await screen.findByText("Yes");
    expect(screen.queryByRole("button", { name: /tap to speak|speak instead/i })).not.toBeInTheDocument();
  });
});
