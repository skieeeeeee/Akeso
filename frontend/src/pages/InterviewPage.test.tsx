import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { InterviewPage } from "./InterviewPage";
import { AI_STATUS_OFF, PREFERENCES, interviewView, question } from "@/test/fixtures";
import {
  SESSION,
  errorResponse,
  jsonResponse,
  renderWithProviders,
  route,
  signInForTest,
  stubFetch,
} from "@/test/utils";

function stubInterview(
  view = interviewView(),
  extra: ReturnType<typeof route>[] = [],
  preferences = PREFERENCES,
) {
  stubFetch([
    ...extra,
    route("/interview/ai-status", () => jsonResponse(AI_STATUS_OFF)),
    route("/interview/start", () => jsonResponse(view), "POST"),
    route("/auth/me", () => jsonResponse(SESSION)),
    route("/accessibility/preferences", () => jsonResponse(preferences)),
  ]);
}

beforeEach(signInForTest);
afterEach(() => vi.unstubAllGlobals());

describe("InterviewPage — one question at a time", () => {
  it("shows the current question with its explanation and progress", async () => {
    stubInterview();
    renderWithProviders(<InterviewPage />);

    expect(await screen.findByRole("heading", { name: /what problem brings you in/i })).toBeInTheDocument();
    expect(screen.getByText(/describe it in your own words/i)).toBeInTheDocument();
    expect(screen.getByText(/part 1 of 9/i)).toBeInTheDocument();
    expect(screen.getByRole("progressbar")).toHaveAttribute("aria-valuenow", "0");
  });

  it("offers quick-pick answers and submits one on tap", async () => {
    const user = userEvent.setup();
    const answer = vi.fn((_url: string, _init?: RequestInit) =>
      jsonResponse(interviewView({ question: question({ id: "q_duration", instance_key: "q_duration" }) })),
    );
    stubInterview(interviewView(), [route("/answer", answer, "POST")]);
    renderWithProviders(<InterviewPage />);

    // Wait for the question to be interactive before clicking: the page
    // renders a loading panel until preferences resolve.
    const chip = await screen.findByRole("button", { name: "Chest pain" });
    await waitFor(() => expect(chip).toBeEnabled());
    await user.click(chip);

    // Assert on the user-visible outcome first, then on what was sent.
    await waitFor(() => expect(answer).toHaveBeenCalled(), { timeout: 5000 });
    const body = JSON.parse(answer.mock.calls[0]![1]!.body as string);
    expect(body).toMatchObject({
      instance_key: "q_chief_complaint",
      text: "Chest pain",
      input_method: "touch",
    });
  });

  it("submits a typed answer as text", async () => {
    const user = userEvent.setup();
    const answer = vi.fn((_url: string, _init?: RequestInit) => jsonResponse(interviewView()));
    stubInterview(interviewView(), [route("/answer", answer, "POST")]);
    renderWithProviders(<InterviewPage />);

    const field = await screen.findByLabelText(/what problem brings you in/i);
    await user.type(field, "Stomach pain");
    await user.click(screen.getByRole("button", { name: /^continue$/i }));

    await waitFor(() => expect(answer).toHaveBeenCalled());
    const body = JSON.parse(answer.mock.calls[0]![1]!.body as string);
    expect(body.text).toBe("Stomach pain");
    expect(body.input_method).toBe("text");
  });

  it("renders a choice question as tappable options", async () => {
    stubInterview(
      interviewView({
        question: question({
          id: "q_duration",
          instance_key: "q_duration",
          kind: "single_choice",
          text: "How long have you had this?",
          suggestions: [],
          options: [
            { value: "2-3 days", label: "2–3 days", icon: null },
            { value: "About a week", label: "About a week", icon: null },
          ],
        }),
      }),
    );
    renderWithProviders(<InterviewPage />);

    expect(await screen.findByRole("radio", { name: "2–3 days" })).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: "About a week" })).toBeInTheDocument();
  });

  it("labels a per-item follow-up with what it is about", async () => {
    stubInterview(
      interviewView({
        question: question({
          id: "q_condition_medicine",
          instance_key: "q_condition_medicine::Diabetes",
          kind: "yes_no",
          text: "Are you currently taking medicine for Diabetes?",
          about: "Diabetes",
          suggestions: [],
          options: [
            { value: "yes", label: "Yes", icon: "check" },
            { value: "no", label: "No", icon: "minus" },
          ],
        }),
      }),
    );
    renderWithProviders(<InterviewPage />);

    expect(await screen.findByText(/about diabetes/i)).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /taking medicine for diabetes/i }),
    ).toBeInTheDocument();
  });

  it("marks an AI-suggested follow-up as such", async () => {
    stubInterview(
      interviewView({ question: question({ is_ai_suggested: true, suggestions: [] }) }),
    );
    renderWithProviders(<InterviewPage />);
    expect(await screen.findByText(/follow-up question/i)).toBeInTheDocument();
  });

  it("shows the retry hint when an answer was not understood", async () => {
    stubInterview(
      interviewView({ retry_hint: "Sorry, I did not catch that. Please try again." }),
    );
    renderWithProviders(<InterviewPage />);
    expect(await screen.findByText(/did not catch that/i)).toBeInTheDocument();
  });

  it("says so when AI assistance is unavailable, and reassures about progress", async () => {
    stubInterview(interviewView({ ai_fallback_active: true }));
    renderWithProviders(<InterviewPage />);

    const notice = await screen.findByText(/smart assistance is unavailable/i);
    expect(notice).toBeInTheDocument();
    expect(notice.textContent).toMatch(/nothing you have answered is lost/i);
    // The question is still shown — a fallback is not a dead end.
    expect(screen.getByRole("heading", { name: /what problem brings you in/i })).toBeInTheDocument();
  });

  it("lets the patient go back", async () => {
    const user = userEvent.setup();
    const back = vi.fn((_url: string, _init?: RequestInit) => jsonResponse(interviewView()));
    stubInterview(
      interviewView({ progress: { ...interviewView().progress, answered: 3, percent: 20 } }),
      [route("/back", back, "POST")],
    );
    renderWithProviders(<InterviewPage />);

    await user.click(await screen.findByRole("button", { name: /back/i }));
    await waitFor(() => expect(back).toHaveBeenCalled());
  });

  it("disables back on the very first question", async () => {
    stubInterview();
    renderWithProviders(<InterviewPage />);
    expect(await screen.findByRole("button", { name: /back/i })).toBeDisabled();
  });

  it("shows a completion screen with the next steps", async () => {
    stubInterview(
      interviewView({
        question: null,
        complete: true,
        status: "awaiting_review",
        progress: { ...interviewView().progress, answered: 18, percent: 100 },
      }),
    );
    renderWithProviders(<InterviewPage />);

    expect(await screen.findByText(/that is everything we need/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /previous medical records/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /check your information/i })).toBeInTheDocument();
  });

  it("surfaces a submission failure without losing the question", async () => {
    const user = userEvent.setup();
    stubInterview(interviewView(), [
      route("/answer", () => errorResponse("Could not save just now", 503, "database_unavailable"), "POST"),
    ]);
    renderWithProviders(<InterviewPage />);

    await user.click(await screen.findByRole("button", { name: "Fever" }));

    expect(await screen.findByText("Could not save just now")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /what problem brings you in/i })).toBeInTheDocument();
  });

  it("recovers from a failed start with a retry", async () => {
    stubFetch([
      route("/interview/ai-status", () => jsonResponse(AI_STATUS_OFF)),
      route("/interview/start", () => errorResponse("Server unavailable", 503, "upstream"), "POST"),
      route("/auth/me", () => jsonResponse(SESSION)),
      route("/accessibility/preferences", () => jsonResponse(PREFERENCES)),
    ]);
    renderWithProviders(<InterviewPage />);

    expect(await screen.findByText("Server unavailable")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
  });
});

describe("InterviewPage — easy mode", () => {
  it("keeps one question per screen and hides the extra offer", async () => {
    stubInterview(interviewView(), [], { ...PREFERENCES, interface_mode: "easy" });
    renderWithProviders(<InterviewPage />);

    await screen.findByRole("heading", { name: /what problem brings you in/i });
    // The AYUSH upsell card is standard-mode only, to keep one task per screen.
    expect(screen.queryByText(/include ayurveda questions/i)).not.toBeInTheDocument();
  });
});
