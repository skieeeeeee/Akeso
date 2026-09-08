import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AssessmentPage } from "./AssessmentPage";
import { ASSESSMENT_CONTENT, PREFERENCES } from "@/test/fixtures";
import {
  SESSION,
  errorResponse,
  jsonResponse,
  renderWithProviders,
  route,
  signInForTest,
  stubFetch,
} from "@/test/utils";

const CONTENT_ROUTE = route("/accessibility/content", () => jsonResponse(ASSESSMENT_CONTENT));
const SESSION_ROUTE = route("/auth/me", () => jsonResponse(SESSION));

function stubStandardMode(extra: ReturnType<typeof route>[] = []) {
  stubFetch([
    ...extra,
    CONTENT_ROUTE,
    SESSION_ROUTE,
    route("/accessibility/preferences", () => jsonResponse(PREFERENCES)),
  ]);
}

function stubEasyMode(extra: ReturnType<typeof route>[] = []) {
  stubFetch([
    ...extra,
    CONTENT_ROUTE,
    SESSION_ROUTE,
    route("/accessibility/preferences", () =>
      jsonResponse({ ...PREFERENCES, interface_mode: "easy", font_size: "large" }),
    ),
  ]);
}

beforeEach(signInForTest);
afterEach(() => vi.unstubAllGlobals());

describe("AssessmentPage — standard mode", () => {
  it("shows every question on one screen", async () => {
    stubStandardMode();
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en);
    for (const question of ASSESSMENT_CONTENT.questions) {
      expect(screen.getByText(question.prompt.en)).toBeInTheDocument();
    }
  });

  it("cannot continue until every required question is answered", async () => {
    const user = userEvent.setup();
    stubStandardMode();
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en);
    const continueButton = screen.getByRole("button", { name: /continue/i });
    expect(continueButton).toBeDisabled();

    // Answer four of the five required questions.
    await user.click(screen.getByRole("radio", { name: /very comfortable/i }));
    await user.click(screen.getByRole("radio", { name: /by touching options/i }));
    const noDifficulty = screen.getAllByRole("radio", { name: /no difficulty/i });
    await user.click(noDifficulty[0]!);
    await user.click(noDifficulty[1]!);
    expect(screen.getByRole("button", { name: /continue/i })).toBeDisabled();

    // The last one enables it.
    await user.click(noDifficulty[2]!);
    await waitFor(() =>
      expect(screen.getByRole("button", { name: /continue/i })).toBeEnabled(),
    );
  });

  it("marks the optional question as optional and never requires it", async () => {
    stubStandardMode();
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(ASSESSMENT_CONTENT.questions[5]!.prompt.en);
    // The multi-select question is labelled optional.
    expect(screen.getByText(/\(optional\)/i)).toBeInTheDocument();
  });

  it("submits the collected answers", async () => {
    const user = userEvent.setup();
    const submit = vi.fn((_url: string, _init?: RequestInit) =>
      jsonResponse({
        assessment_id: "a1",
        recommendation: { ...PREFERENCES, easy_mode_score: 0, easy_mode_threshold: 3, reasons: [] },
        preferences: PREFERENCES,
        onboarding_status: "preferences_pending",
        next_route: "/onboarding/preferences",
      }),
    );
    stubStandardMode([route("/accessibility/assessment", submit, "POST")]);
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en);
    await user.click(screen.getByRole("radio", { name: /very comfortable/i }));
    await user.click(screen.getByRole("radio", { name: /by touching options/i }));
    for (const radio of screen.getAllByRole("radio", { name: /no difficulty/i })) {
      await user.click(radio);
    }
    await user.click(screen.getByRole("button", { name: /continue/i }));

    await waitFor(() => expect(submit).toHaveBeenCalled());
  });

  it("shows a retryable error when the questions cannot be loaded", async () => {
    stubFetch([
      route("/accessibility/content", () => errorResponse("Server unavailable", 503, "upstream_unavailable")),
      SESSION_ROUTE,
      route("/accessibility/preferences", () => jsonResponse(PREFERENCES)),
    ]);
    renderWithProviders(<AssessmentPage />);

    expect(await screen.findByText("Server unavailable")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
  });

  it("surfaces a submission failure without losing the answers", async () => {
    const user = userEvent.setup();
    stubStandardMode([
      route("/accessibility/assessment", () => errorResponse("Could not save just now", 503, "database_unavailable"), "POST"),
    ]);
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en);
    await user.click(screen.getByRole("radio", { name: /very comfortable/i }));
    await user.click(screen.getByRole("radio", { name: /by touching options/i }));
    for (const radio of screen.getAllByRole("radio", { name: /no difficulty/i })) {
      await user.click(radio);
    }
    await user.click(screen.getByRole("button", { name: /continue/i }));

    expect(await screen.findByText("Could not save just now")).toBeInTheDocument();
    // The chosen answer is still selected.
    expect(screen.getByRole("radio", { name: /very comfortable/i })).toBeChecked();
  });
});

describe("AssessmentPage — easy mode", () => {
  it("shows one question at a time with its position", async () => {
    stubEasyMode();
    renderWithProviders(<AssessmentPage />);

    // Wait for the easy-mode layout specifically before asserting.
    await screen.findByText(/question 1 of 6/i);
    expect(screen.getByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en)).toBeInTheDocument();
    // Only the first question is on screen.
    expect(screen.queryByText(ASSESSMENT_CONTENT.questions[1]!.prompt.en)).not.toBeInTheDocument();
  });

  it("advances one question at a time and allows going back", async () => {
    const user = userEvent.setup();
    stubEasyMode();
    renderWithProviders(<AssessmentPage />);

    await screen.findByText(/question 1 of 6/i);
    // Cannot advance without answering the visible question.
    expect(screen.getByRole("button", { name: /continue/i })).toBeDisabled();

    await user.click(screen.getByRole("radio", { name: /very comfortable/i }));
    await user.click(screen.getByRole("button", { name: /continue/i }));

    expect(await screen.findByText(ASSESSMENT_CONTENT.questions[1]!.prompt.en)).toBeInTheDocument();
    expect(screen.getByText(/question 2 of 6/i)).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /back/i }));
    expect(await screen.findByText(ASSESSMENT_CONTENT.questions[0]!.prompt.en)).toBeInTheDocument();
    // The earlier answer is remembered.
    expect(screen.getByRole("radio", { name: /very comfortable/i })).toBeChecked();
  });
});
