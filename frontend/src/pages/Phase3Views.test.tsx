import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { HomePage } from "./HomePage";
import { VisitPage } from "./VisitPage";
import { VisitReviewPage } from "./VisitReviewPage";
import { SettingsPage } from "./SettingsPage";
import { AyushPage } from "./AyushPage";
import {
  ASSESSMENT_CONTENT,
  AYUSH_CONTENT,
  ENCOUNTER_REVIEW,
  HOME,
  PREFERENCES,
  SAFETY_ACTIVE,
  encounterView,
  question,
} from "@/test/fixtures";
import {
  SESSION,
  errorResponse,
  jsonResponse,
  renderWithProviders,
  route,
  signInForTest,
  stubFetch,
} from "@/test/utils";

const BASE = [
  route("/auth/me", () => jsonResponse(SESSION)),
  route("/accessibility/preferences", () => jsonResponse(PREFERENCES)),
];

beforeEach(signInForTest);
afterEach(() => vi.unstubAllGlobals());

describe("HomePage — the returning patient", () => {
  it("greets them and shows their health summary, not a blank screen", async () => {
    stubFetch([route("/patients/me/home", () => jsonResponse(HOME)), ...BASE]);
    renderWithProviders(<HomePage />);

    expect(await screen.findByRole("heading", { name: /welcome back, rajesh/i })).toBeInTheDocument();
    expect(screen.getByText("Type 2 diabetes mellitus")).toBeInTheDocument();
    expect(screen.getByText("Metformin 500 mg")).toBeInTheDocument();
    expect(screen.getByText("Sulfa drugs")).toBeInTheDocument();
    expect(screen.getByText(/2 visits recorded/i)).toBeInTheDocument();
    // "City Lab" appears both as a record and as a timeline event.
    expect(screen.getAllByText("City Lab").length).toBeGreaterThan(0);
    expect(screen.getByText(/routine diabetes review/i)).toBeInTheDocument();
  });

  it("makes starting a new visit the primary action", async () => {
    stubFetch([route("/patients/me/home", () => jsonResponse(HOME)), ...BASE]);
    renderWithProviders(<HomePage />);

    expect(
      await screen.findByRole("heading", { name: /start a new health visit/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/we already have your history/i)).toBeInTheDocument();
    const cta = screen.getAllByRole("link").find((link) => link.getAttribute("href") === "/visit");
    expect(cta).toBeDefined();
  });

  it("offers to resume an unfinished visit rather than starting a second", async () => {
    stubFetch([
      route("/patients/me/home", () =>
        jsonResponse({
          ...HOME,
          visit_in_progress: {
            id: "enc-9",
            complaint: "Back pain",
            started_at: "2026-09-07T09:00:00Z",
            is_urgent: false,
          },
        }),
      ),
      ...BASE,
    ]);
    renderWithProviders(<HomePage />);

    expect(await screen.findByRole("heading", { name: /continue your visit/i })).toBeInTheDocument();
    expect(screen.getByText(/“Back pain”/)).toBeInTheDocument();
  });

  it("shows the urgent banner when an in-progress visit is flagged", async () => {
    stubFetch([
      route("/patients/me/home", () =>
        jsonResponse({
          ...HOME,
          visit_in_progress: { id: "enc-9", complaint: null, started_at: null, is_urgent: true },
        }),
      ),
      ...BASE,
    ]);
    renderWithProviders(<HomePage />);
    // Banner text plus its badge both match.
    expect((await screen.findAllByText(/marked urgent/i)).length).toBeGreaterThan(0);
  });

  it("uses a real empty state with an action when there are no records", async () => {
    stubFetch([
      route("/patients/me/home", () =>
        jsonResponse({ ...HOME, recent_documents: [], document_count: 0 }),
      ),
      ...BASE,
    ]);
    renderWithProviders(<HomePage />);

    expect(await screen.findByText(/have not added any medical records/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /choose a photo or pdf/i })).toBeInTheDocument();
  });

  it("nudges an incomplete profile toward the exact next step", async () => {
    stubFetch([
      route("/patients/me/home", () =>
        jsonResponse({
          ...HOME,
          profile_complete: false,
          onboarding: { ...HOME.onboarding, is_complete: false, next_route: "/onboarding/assessment" },
        }),
      ),
      ...BASE,
    ]);
    renderWithProviders(<HomePage />);

    const link = await screen.findByRole("link", { name: /finish setting up your profile/i });
    expect(link).toHaveAttribute("href", "/onboarding/assessment");
  });

  it("is retryable when the request fails", async () => {
    stubFetch([
      route("/patients/me/home", () => errorResponse("Server unavailable", 503, "upstream")),
      ...BASE,
    ]);
    renderWithProviders(<HomePage />);
    expect(await screen.findByText("Server unavailable")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
  });
});

describe("VisitPage — asks about today only", () => {
  it("asks the opening question and shows history as context", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(encounterView()), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);

    expect(await screen.findByRole("heading", { name: /what brings you here today/i })).toBeInTheDocument();
    // History is offered read-only, with an explanation of why.
    expect(screen.getByText(/we already know about/i)).toBeInTheDocument();
    expect(screen.getByText(/will not be asked about these again/i)).toBeInTheDocument();
    expect(screen.getByText("Type 2 diabetes mellitus")).toBeInTheDocument();
    expect(screen.getByText(/about today only/i)).toBeInTheDocument();
  });

  it("offers common symptom suggestions and free text", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(encounterView()), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);

    expect(await screen.findByRole("button", { name: "Fever" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Cough" })).toBeInTheDocument();
    // Free text is never removed as an option.
    expect(screen.getByLabelText(/what brings you here today/i)).toBeInTheDocument();
  });

  it("submits an answer for the current visit", async () => {
    const user = userEvent.setup();
    const answer = vi.fn((_url: string, _init?: RequestInit) =>
      jsonResponse(encounterView({ question: question({ id: "e_onset", instance_key: "e_onset" }) })),
    );
    stubFetch([
      route("/answer", answer, "POST"),
      route("/encounters/start", () => jsonResponse(encounterView()), "POST"),
      ...BASE,
    ]);
    renderWithProviders(<VisitPage />);

    const chip = await screen.findByRole("button", { name: "Fever" });
    await waitFor(() => expect(chip).toBeEnabled());
    await user.click(chip);

    await waitFor(() => expect(answer).toHaveBeenCalled(), { timeout: 5000 });
    expect(answer.mock.calls[0]![0]).toContain("/encounters/enc-1/answer");
  });

  it("ends by sending the patient to review, not straight to submission", async () => {
    stubFetch([
      route("/encounters/start", () =>
        jsonResponse(
          encounterView({
            question: null,
            complete: true,
            progress: { ...encounterView().progress, answered: 9, percent: 100 },
          }),
        ),
        "POST",
      ),
      ...BASE,
    ]);
    renderWithProviders(<VisitPage />);

    expect(await screen.findByText(/that is everything for today/i)).toBeInTheDocument();
    const link = screen.getByRole("link", { name: /check and submit/i });
    expect(link).toHaveAttribute("href", "/visit/enc-1/review");
  });
});

describe("VisitPage — red-flag safety", () => {
  const URGENT = encounterView({ priority: "urgent", safety: SAFETY_ACTIVE });

  it("interrupts with the emergency screen as soon as a flag is raised", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(URGENT), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);

    expect(
      await screen.findByRole("heading", { name: /speak to healthcare staff now/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/may require urgent medical attention/i)).toBeInTheDocument();
    // It says plainly that this is not a diagnosis.
    expect(screen.getByText(/does not confirm a medical condition/i)).toBeInTheDocument();
    expect(screen.getByText(/inform nearby healthcare staff/i)).toBeInTheDocument();
    // The question itself is replaced while this shows.
    expect(screen.queryByLabelText(/what brings you here today/i)).not.toBeInTheDocument();
  });

  it("names no condition anywhere on the emergency screen", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(URGENT), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);
    await screen.findByRole("heading", { name: /speak to healthcare staff now/i });

    const text = document.body.textContent?.toLowerCase() ?? "";
    for (const forbidden of ["heart attack", "stroke", "you have", "diagnosed"]) {
      expect(text).not.toContain(forbidden);
    }
  });

  it("quotes the patient's own words as the reason", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(URGENT), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);
    expect(await screen.findByText(/crushing chest pain/i)).toBeInTheDocument();
  });

  it("offers both actions and says the flag cannot be switched off", async () => {
    stubFetch([route("/encounters/start", () => jsonResponse(URGENT), "POST"), ...BASE]);
    renderWithProviders(<VisitPage />);

    expect(await screen.findByRole("button", { name: /i need immediate assistance/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /continue answering while waiting/i })).toBeInTheDocument();
    expect(screen.getByText(/cannot be turned off from here/i)).toBeInTheDocument();
  });

  it("continuing keeps the urgent state visible on every screen", async () => {
    const user = userEvent.setup();
    const acknowledged = encounterView({
      priority: "urgent",
      safety: { ...SAFETY_ACTIVE, acknowledged: true },
    });
    stubFetch([
      route("/safety/acknowledge", () => jsonResponse(acknowledged), "POST"),
      route("/encounters/start", () => jsonResponse(URGENT), "POST"),
      ...BASE,
    ]);
    renderWithProviders(<VisitPage />);

    await user.click(
      await screen.findByRole("button", { name: /continue answering while waiting/i }),
    );

    // Back to the interview, but the urgent banner persists.
    expect(await screen.findByText(/marked urgent — please stay near the staff desk/i)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /what brings you here today/i })).toBeInTheDocument();
  });

  it("requesting assistance confirms staff were notified", async () => {
    const user = userEvent.setup();
    stubFetch([
      route("/safety/assistance", () => jsonResponse(URGENT), "POST"),
      route("/encounters/start", () => jsonResponse(URGENT), "POST"),
      ...BASE,
    ]);
    renderWithProviders(<VisitPage />);

    await user.click(await screen.findByRole("button", { name: /i need immediate assistance/i }));
    expect(await screen.findByText(/staff have been notified/i)).toBeInTheDocument();
  });

  it("an already-acknowledged flag does not re-interrupt", async () => {
    stubFetch([
      route("/encounters/start", () =>
        jsonResponse(
          encounterView({
            priority: "urgent",
            safety: { ...SAFETY_ACTIVE, acknowledged: true },
          }),
        ),
        "POST",
      ),
      ...BASE,
    ]);
    renderWithProviders(<VisitPage />);

    expect(await screen.findByRole("heading", { name: /what brings you here today/i })).toBeInTheDocument();
    expect(screen.getAllByText(/marked urgent/i).length).toBeGreaterThan(0);
  });
});

describe("VisitReviewPage", () => {
  const ROUTES = [
    route("/encounters/enc-1/review", () => jsonResponse(ENCOUNTER_REVIEW)),
    ...BASE,
  ];

  function render() {
    // Mounted under its real route pattern so `useParams` resolves.
    return renderWithProviders(<VisitReviewPage />, {
      route: "/visit/enc-1/review",
      path: "/visit/:encounterId/review",
    });
  }

  const AYURVEDIC = {
    ...ENCOUNTER_REVIEW,
    ayush: {
      count: 24,
      total: 24,
      entries: [
        {
          group: "dashavidha",
          term: "Prakriti",
          question: "Which best describes your natural build?",
          answer: "Medium build, sharp and warm",
        },
        {
          group: "ashtasthana",
          term: "Nadi",
          question: "How does your pulse usually feel?",
          answer: "Steady",
        },
        { group: "ahara", term: "", question: "", answer: "Mostly home-cooked" },
      ],
    },
  };

  it("reports the Ayurvedic examination the patient answered", async () => {
    // An Ayurvedic visit asks around twenty more questions, and those answers
    // are stored on the assessment rather than the profile. Without this the
    // patient answers thirty-three questions and the review screen shows five.
    stubFetch([route("/encounters/enc-1/review", () => jsonResponse(AYURVEDIC)), ...BASE]);
    render();

    expect(
      await screen.findByRole("heading", { name: /ayurvedic examination you answered/i }),
    ).toBeInTheDocument();
    expect(screen.getByText("24 of 24 factors recorded")).toBeInTheDocument();
    expect(screen.getByText("Medium build, sharp and warm")).toBeInTheDocument();
    expect(screen.getByText(/Prakriti/)).toBeInTheDocument();
    // Diet is a multi-select, so it reads as a chip with no question row.
    expect(screen.getByText("Mostly home-cooked")).toBeInTheDocument();
    // Never presented as a finding — the card carries its own caveat, on top
    // of the page-level disclaimer.
    expect(screen.getAllByText(/not a diagnosis/i).length).toBeGreaterThan(1);
  });

  it("omits the examination card for an allopathic visit", async () => {
    stubFetch(ROUTES);
    render();

    expect(await screen.findByText(/what you told us today/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: /ayurvedic examination/i }),
    ).not.toBeInTheDocument();
  });

  it("shows today's concern, today's answers and history separately", async () => {
    stubFetch(ROUTES);
    render();

    // Appears as the concern heading and again as the first answer.
    expect((await screen.findAllByText("Stomach pain since yesterday")).length).toBeGreaterThan(0);
    expect(screen.getByText(/what you told us today/i)).toBeInTheDocument();
    expect(screen.getByText("Yesterday")).toBeInTheDocument();
    // Existing history is present, labelled, and explicitly not editable here.
    expect(screen.getByText(/we already know about/i)).toBeInTheDocument();
    expect(screen.getByText(/editing this happens in your health history, not here/i)).toBeInTheDocument();
  });

  it("shows severity as a metric, not as another answer row", async () => {
    stubFetch(ROUTES);
    render();
    expect(await screen.findByText(/how much it troubles you/i)).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
    expect(screen.getByText(/out of 10/i)).toBeInTheDocument();
  });

  it("counts skipped questions instead of listing them", async () => {
    stubFetch(ROUTES);
    render();
    expect(await screen.findByText(/3 questions you chose to skip/i)).toBeInTheDocument();
    // No wall of "None reported".
    expect(screen.queryByText(/none reported/i)).not.toBeInTheDocument();
  });

  it("shows one urgent indicator, not two", async () => {
    stubFetch([
      route("/encounters/enc-1/review", () =>
        jsonResponse({ ...ENCOUNTER_REVIEW, safety: SAFETY_ACTIVE, priority: "urgent" }),
      ),
      ...BASE,
    ]);
    render();
    // Exactly one urgent banner, and no separate header badge beside it.
    const banners = await screen.findAllByText(/please stay near the staff desk/i, {
      selector: "p",
    });
    expect(banners).toHaveLength(1);
  });

  it("explains why a low severity can still be urgent", async () => {
    stubFetch([
      route("/encounters/enc-1/review", () =>
        jsonResponse({ ...ENCOUNTER_REVIEW, severity: "2/10", safety: SAFETY_ACTIVE, priority: "urgent" }),
      ),
      ...BASE,
    ]);
    render();
    expect(await screen.findByText(/not what made your visit urgent/i)).toBeInTheDocument();
  });

  it("shows the summary and says it is not a diagnosis", async () => {
    stubFetch(ROUTES);
    render();
    expect(await screen.findByText(/returns reporting stomach pain/i)).toBeInTheDocument();
    expect(screen.getByText(/not a diagnosis, and a healthcare professional/i)).toBeInTheDocument();
  });

  it("keeps submission disabled until all three confirmations are given", async () => {
    const user = userEvent.setup();
    stubFetch(ROUTES);
    render();

    const submitButton = await screen.findByRole("button", { name: /send to the care team/i });
    expect(submitButton).toBeDisabled();

    await user.click(screen.getByLabelText(/current symptoms were recorded correctly/i));
    expect(submitButton).toBeDisabled();
    await user.click(screen.getByLabelText(/reviewed the information above/i));
    expect(submitButton).toBeDisabled();
    await user.click(screen.getByLabelText(/support my healthcare visit/i));
    await waitFor(() => expect(submitButton).toBeEnabled());
  });

  it("submits the three confirmations", async () => {
    const user = userEvent.setup();
    const submit = vi.fn((_url: string, _init?: RequestInit) =>
      jsonResponse({
        encounter_id: "enc-1",
        status: "completed",
        priority: "routine",
        submitted_at: "2026-09-07T12:00:00Z",
        message: { en: "Your visit details have been sent.", hi: "भेज दी गई।" },
      }),
    );
    stubFetch([route("/submit", submit, "POST"), ...ROUTES]);
    render();

    await user.click(await screen.findByLabelText(/current symptoms were recorded correctly/i));
    await user.click(screen.getByLabelText(/reviewed the information above/i));
    await user.click(screen.getByLabelText(/support my healthcare visit/i));
    await user.click(screen.getByRole("button", { name: /send to the care team/i }));

    await waitFor(() => expect(submit).toHaveBeenCalled(), { timeout: 5000 });
    expect(JSON.parse(submit.mock.calls[0]![1]!.body as string)).toEqual({
      symptoms_correct: true,
      reviewed_information: true,
      understands_use: true,
    });
    expect(await screen.findByText(/your visit has been sent/i)).toBeInTheDocument();
  });

  it("an already-submitted visit cannot be submitted again", async () => {
    stubFetch([
      route("/encounters/enc-1/review", () =>
        jsonResponse({ ...ENCOUNTER_REVIEW, submitted_at: "2026-09-07T12:00:00Z" }),
      ),
      ...BASE,
    ]);
    render();

    expect(await screen.findByText(/already been sent/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /send to the care team/i })).not.toBeInTheDocument();
  });

  it("surfaces missing information with a way back", async () => {
    stubFetch([
      route("/encounters/enc-1/review", () =>
        jsonResponse({ ...ENCOUNTER_REVIEW, missing: ["history_of_present_illness"] }),
      ),
      ...BASE,
    ]);
    render();

    expect(await screen.findByText(/still needed/i)).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: /change today's answers/i })[0]).toHaveAttribute(
      "href",
      "/visit",
    );
  });

  it("carries the urgent banner through to review", async () => {
    stubFetch([
      route("/encounters/enc-1/review", () =>
        jsonResponse({ ...ENCOUNTER_REVIEW, safety: SAFETY_ACTIVE, priority: "urgent" }),
      ),
      ...BASE,
    ]);
    render();
    expect((await screen.findAllByText(/marked urgent/i)).length).toBeGreaterThan(0);
  });
});

describe("AYUSH discoverability and depth", () => {
  it("is reachable from the home screen, not buried in a visit", async () => {
    stubFetch([route("/patients/me/home", () => jsonResponse(HOME)), ...BASE]);
    renderWithProviders(<HomePage />);

    const link = await screen.findByRole("link", { name: /open assessment/i });
    expect(link).toHaveAttribute("href", "/ayush");
    expect(screen.getByText(/record your constitution/i)).toBeInTheDocument();
  });

  it("renders all three examination groups", async () => {
    stubFetch([
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);

    expect(await screen.findByRole("heading", { name: /ten-fold examination/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /eight-fold examination/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /digestion, sleep and routine/i })).toBeInTheDocument();
  });

  it("shows the Sanskrit term beside a plain-language prompt", async () => {
    stubFetch([
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);

    expect(await screen.findByText(/how does your pulse usually feel/i)).toBeInTheDocument();
    expect(screen.getByText(/Nadi ·/)).toBeInTheDocument();
  });

  it("says the app does not interpret these answers", async () => {
    stubFetch([
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);
    expect(
      await screen.findByText(/nothing here is assessed or interpreted by the app/i),
    ).toBeInTheDocument();
  });

  it("counts progress against the full factor total", async () => {
    stubFetch([
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);
    expect(await screen.findByText(/0 \/ 24 factors recorded/i)).toBeInTheDocument();
  });

  it("lets a sensitive question be declined", async () => {
    stubFetch([
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);
    expect(
      await screen.findByRole("radio", { name: /would rather not say/i }),
    ).toBeInTheDocument();
  });

  it("submits every group together", async () => {
    const user = userEvent.setup();
    const save = vi.fn((_url: string, _init?: RequestInit) => jsonResponse({}));
    stubFetch([
      route("/ayush", save, "PUT"),
      route("/ayush/content", () => jsonResponse(AYUSH_CONTENT)),
      route("/ayush", () => jsonResponse(null)),
      ...BASE,
    ]);
    renderWithProviders(<AyushPage />);

    await user.click(await screen.findByRole("radio", { name: /thin build/i }));
    await user.click(screen.getByRole("radio", { name: /normal and steady/i }));
    await user.click(screen.getByRole("button", { name: /^save$/i }));

    await waitFor(() => expect(save).toHaveBeenCalled(), { timeout: 5000 });
    const body = JSON.parse(save.mock.calls[0]![1]!.body as string);
    expect(body.dashavidha).toEqual({ prakriti: "vata" });
    expect(body.ashtasthana).toEqual({ nadi: "normal" });
    expect(body).toHaveProperty("lifestyle");
  });
});

describe("SettingsPage", () => {
  const ROUTES = [
    route("/accessibility/content", () => jsonResponse(ASSESSMENT_CONTENT)),
    ...BASE,
  ];

  it("lets the patient change settings without retaking the assessment", async () => {
    stubFetch(ROUTES);
    renderWithProviders(<SettingsPage />);

    expect(await screen.findByRole("heading", { name: /^settings$/i })).toBeInTheDocument();
    // Retaking is offered, not required.
    expect(screen.getByRole("link", { name: /retake the comfort check/i })).toBeInTheDocument();
    expect(screen.getByText(/optional\. we will suggest settings again/i)).toBeInTheDocument();
  });

  it("persists a change immediately", async () => {
    const user = userEvent.setup();
    // The stub holds state, so the refetch after saving returns the saved
    // value rather than reverting — as the real API would.
    let stored = { ...PREFERENCES };
    const save = vi.fn((_url: string, init?: RequestInit) => {
      stored = { ...stored, ...JSON.parse(String(init?.body)), source: "customized" };
      return jsonResponse(stored);
    });
    stubFetch([
      route("/accessibility/preferences", save, "PUT"),
      route("/accessibility/preferences", () => jsonResponse(stored)),
      route("/accessibility/content", () => jsonResponse(ASSESSMENT_CONTENT)),
      route("/auth/me", () => jsonResponse(SESSION)),
    ]);
    renderWithProviders(<SettingsPage />);

    await user.click(await screen.findByRole("radio", { name: /^large$/i }));

    await waitFor(() => expect(save).toHaveBeenCalled(), { timeout: 5000 });
    const body = JSON.parse(save.mock.calls[0]![1]!.body as string);
    expect(body.font_size).toBe("large");
    // Applied straight away so the effect is visible.
    await waitFor(() => expect(document.documentElement.dataset.fontSize).toBe("large"));
  });

  it("offers both languages", async () => {
    stubFetch(ROUTES);
    renderWithProviders(<SettingsPage />);
    expect(await screen.findByRole("radio", { name: /english/i })).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: /हिन्दी/ })).toBeInTheDocument();
  });
});
