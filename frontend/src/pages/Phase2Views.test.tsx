import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DocumentCard } from "@/features/documents/DocumentCard";
import { TimelinePage } from "./TimelinePage";
import { ReviewPage } from "./ReviewPage";
import {
  PREFERENCES,
  STRUCTURED_HISTORY,
  TIMELINE,
  interviewView,
  medicalDocument,
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

describe("DocumentCard — processing states", () => {
  it("offers to read a document that is only stored", async () => {
    stubFetch(BASE);
    renderWithProviders(
      <DocumentCard document={medicalDocument({ processing_status: "pending", extracted_items: [] })} />,
    );
    expect(await screen.findByRole("button", { name: /read this document/i })).toBeInTheDocument();
  });

  it("shows findings as information found, not as facts", async () => {
    stubFetch(BASE);
    renderWithProviders(<DocumentCard document={medicalDocument()} />);

    expect(await screen.findByText(/information found in this document/i)).toBeInTheDocument();
    expect(screen.getByText(/it is not a diagnosis/i)).toBeInTheDocument();
    expect(screen.getByText("Haemoglobin")).toBeInTheDocument();
    // A flag derived from the printed range, phrased as a comparison.
    expect(screen.getByText(/below the printed range/i)).toBeInTheDocument();
    expect(screen.getByText(/compared only against the range printed/i)).toBeInTheDocument();
  });

  it("a finding can be accepted", async () => {
    const user = userEvent.setup();
    const review = vi.fn((_url: string, _init?: RequestInit) => jsonResponse({}));
    stubFetch([route("/findings/", review, "POST"), ...BASE]);
    renderWithProviders(<DocumentCard document={medicalDocument()} />);

    await user.click(await screen.findByRole("button", { name: /that is correct/i }));
    await waitFor(() => expect(review).toHaveBeenCalled());
    expect(JSON.parse(review.mock.calls[0]![1]!.body as string)).toEqual({
      review_state: "accepted",
    });
  });

  it("a finding can be rejected", async () => {
    const user = userEvent.setup();
    const review = vi.fn((_url: string, _init?: RequestInit) => jsonResponse({}));
    stubFetch([route("/findings/", review, "POST"), ...BASE]);
    renderWithProviders(<DocumentCard document={medicalDocument()} />);

    await user.click(await screen.findByRole("button", { name: /that is not right/i }));
    await waitFor(() =>
      expect(JSON.parse(review.mock.calls[0]![1]!.body as string)).toEqual({
        review_state: "rejected",
      }),
    );
  });

  it("an already-reviewed finding shows its state instead of buttons", async () => {
    stubFetch(BASE);
    const document = medicalDocument();
    document.extracted_items![0]!.review_state = "accepted";
    renderWithProviders(<DocumentCard document={document} />);

    expect(await screen.findByText(/confirmed by you/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /that is correct/i })).not.toBeInTheDocument();
  });

  it("a failed document keeps its error and offers a retry", async () => {
    const user = userEvent.setup();
    const retry = vi.fn((_url: string, _init?: RequestInit) => jsonResponse({}));
    stubFetch([route("/retry", retry, "POST"), ...BASE]);
    renderWithProviders(
      <DocumentCard
        document={medicalDocument({
          processing_status: "failed",
          processing_error: "We could not read this document. It is saved and you can try again.",
          extracted_items: [],
        })}
      />,
    );

    expect(await screen.findByText(/could not read this document/i)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /try reading again/i }));
    await waitFor(() => expect(retry).toHaveBeenCalled());
  });

  it("needs_review explains itself and keeps the raw text available", async () => {
    const user = userEvent.setup();
    stubFetch(BASE);
    renderWithProviders(
      <DocumentCard
        document={medicalDocument({
          processing_status: "needs_review",
          extracted_items: [],
          ocr_text: "Bus ticket Nagpur to Pune",
        })}
      />,
    );

    // The message names the likely cause (handwriting) and reassures the
    // patient that the document is kept and the doctor will read it.
    expect(
      await screen.findByText(/could not pick out medicines or test values/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/your doctor will read it themselves/i)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /show the text we read/i }));
    expect(screen.getByText(/bus ticket nagpur/i)).toBeInTheDocument();
  });
});

describe("TimelinePage", () => {
  it("lists events with their source and a disclaimer", async () => {
    stubFetch([route("/timeline", () => jsonResponse(TIMELINE)), ...BASE]);
    renderWithProviders(<TimelinePage />);

    expect(await screen.findByRole("heading", { name: /medical timeline/i })).toBeInTheDocument();
    expect(screen.getByText("City Lab")).toBeInTheDocument();
    expect(screen.getByText("Haemoglobin")).toBeInTheDocument();
    expect(screen.getByText(/found in city lab/i)).toBeInTheDocument();
    expect(screen.getByText(/it is not a diagnosis/i)).toBeInTheDocument();
    expect(screen.getByText(/needs your check/i)).toBeInTheDocument();
  });

  it("only offers filters that would return something", async () => {
    stubFetch([route("/timeline", () => jsonResponse(TIMELINE)), ...BASE]);
    renderWithProviders(<TimelinePage />);

    expect(await screen.findByRole("button", { name: /records 1/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /tests 1/i })).toBeInTheDocument();
    // No medicines in this fixture, so no medicines chip.
    expect(screen.queryByRole("button", { name: /medicines/i })).not.toBeInTheDocument();
  });

  it("filtering re-queries with the chosen type", async () => {
    const user = userEvent.setup();
    const timeline = vi.fn((_url: string) => jsonResponse(TIMELINE));
    stubFetch([route("/timeline", timeline), ...BASE]);
    renderWithProviders(<TimelinePage />);

    await user.click(await screen.findByRole("button", { name: /tests 1/i }));
    await waitFor(() =>
      expect(timeline.mock.calls.some(([url]) => url.includes("event_type=investigation"))).toBe(true),
    );
  });

  it("an empty timeline points at the interview", async () => {
    stubFetch([
      route("/timeline", () => jsonResponse({ ...TIMELINE, events: [], total: 0, counts: {} })),
      ...BASE,
    ]);
    renderWithProviders(<TimelinePage />);

    expect(await screen.findByText(/nothing here yet/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /start/i })).toBeInTheDocument();
  });

  it("a failure is retryable", async () => {
    stubFetch([
      route("/timeline", () => errorResponse("Server unavailable", 503, "upstream")),
      ...BASE,
    ]);
    renderWithProviders(<TimelinePage />);
    expect(await screen.findByText("Server unavailable")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /try again/i })).toBeInTheDocument();
  });
});

describe("ReviewPage", () => {
  const REVIEW_ROUTES = [
    route("/medical-profile/structured", () => jsonResponse(STRUCTURED_HISTORY)),
    route("/interview/current", () => jsonResponse(interviewView())),
    ...BASE,
  ];

  it("separates what the patient said from what documents say", async () => {
    stubFetch(REVIEW_ROUTES);
    renderWithProviders(<ReviewPage />);

    expect(await screen.findByRole("heading", { name: /check your information/i })).toBeInTheDocument();
    expect(screen.getByText("Chest pain")).toBeInTheDocument();
    expect(screen.getByText("Metformin")).toBeInTheDocument();
    // Every entry is labelled with its provenance.
    expect(screen.getByText(/you said this/i)).toBeInTheDocument();
    expect(screen.getByText(/found in a document/i)).toBeInTheDocument();
    expect(screen.getByText(/found in Dr Mehta/i)).toBeInTheDocument();
  });

  it("surfaces missing sections rather than hiding them", async () => {
    stubFetch(REVIEW_ROUTES);
    renderWithProviders(<ReviewPage />);

    expect(await screen.findByText(/still missing/i)).toBeInTheDocument();
    expect(screen.getByText("Allergies")).toBeInTheDocument();
  });

  it("shows the summary and never claims a diagnosis", async () => {
    stubFetch(REVIEW_ROUTES);
    renderWithProviders(<ReviewPage />);

    expect(await screen.findByText(/patient reports chest pain/i)).toBeInTheDocument();
    expect(screen.getByText(/not a diagnosis, and your doctor/i)).toBeInTheDocument();
  });

  it("each section can be edited", async () => {
    stubFetch(REVIEW_ROUTES);
    renderWithProviders(<ReviewPage />);
    const editLinks = await screen.findAllByRole("link", { name: /change this/i });
    expect(editLinks.length).toBeGreaterThan(0);
    expect(editLinks[0]).toHaveAttribute("href", "/onboarding/medical-profile");
  });

  it("confirming posts to the interview session", async () => {
    const user = userEvent.setup();
    const confirm = vi.fn((_url: string, _init?: RequestInit) => jsonResponse(interviewView()));
    stubFetch([route("/confirm", confirm, "POST"), ...REVIEW_ROUTES]);
    renderWithProviders(<ReviewPage />);

    await user.click(await screen.findByRole("button", { name: /this is correct/i }));
    await waitFor(() => expect(confirm).toHaveBeenCalled());
    expect(confirm.mock.calls[0]![0]).toContain("/interview/sess-1/confirm");
  });
});
