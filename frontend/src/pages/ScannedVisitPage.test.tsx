import { describe, expect, it } from "vitest";
import { screen } from "@testing-library/react";

import { jsonResponse, renderWithProviders, route, stubFetch } from "@/test/utils";
import { ScannedVisitPage } from "@/pages/ScannedVisitPage";

const VISIT = {
  medikiosk: 1,
  generated: "2026-09-09T06:00:00Z",
  patient: { name: "Rajesh Kumar", age: 52, sex: "male" },
  visit: {
    date: "2026-09-09T05:30:00Z",
    type: "follow_up",
    care_system: "ayurveda",
    priority: "routine",
  },
  complaint: "Burning pain in both knees, worse after walking",
  severity: "7/10",
  safety: { status: "none", flags: [] },
  answers: [
    ["What brings you here today?", "Burning pain in both knees"],
    ["When did it start?", "About ten days ago"],
  ],
  history: {
    conditions: ["Type 2 diabetes mellitus"],
    medications: ["Metformin"],
    allergies: ["Sulfa drugs"],
  },
  ayurveda: [["Sara", "Strong and resilient"]],
  documents: ["Dr Mehta prescription"],
  unanswered: 0,
  note: "Patient-reported before consultation. Not a diagnosis.",
};

const routes = (body: unknown, status = 200) => [
  route("/encounters/handoff/", () => jsonResponse(body, status)),
];

describe("the page a clinician lands on after scanning", () => {
  it("shows the visit without anyone signing in", async () => {
    stubFetch(routes(VISIT));
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });

    expect(await screen.findByText("Rajesh Kumar")).toBeTruthy();
    expect(screen.getByText(VISIT.complaint)).toBeTruthy();
    expect(screen.getByText("About ten days ago")).toBeTruthy();
  });

  it("puts the allergy where it cannot be missed", async () => {
    stubFetch(routes(VISIT));
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });
    expect(await screen.findByText("Sulfa drugs")).toBeTruthy();
    expect(screen.getByText("Metformin")).toBeTruthy();
  });

  it("states that this is patient-reported and not a diagnosis", async () => {
    stubFetch(routes(VISIT));
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });
    expect(await screen.findByText(VISIT.note)).toBeTruthy();
  });

  it("shows the ayurvedic examination the QR-only code had to drop", async () => {
    stubFetch(routes(VISIT));
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });
    expect(await screen.findByText("Strong and resilient")).toBeTruthy();
  });

  it("flags an urgent visit as a prompt, never as an assessment", async () => {
    stubFetch(
      routes({
        ...VISIT,
        visit: { ...VISIT.visit, priority: "urgent" },
        safety: {
          status: "active",
          flags: [{ category: "cardiac", reported: "Crushing chest pain" }],
        },
      }),
    );
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });

    expect(await screen.findByText(/flagged for early review/i)).toBeTruthy();
    expect(screen.getByText(/not an assessment/i)).toBeTruthy();
    // The patient's own words are shown; the criteria that matched are not.
    expect(screen.getByText(/Crushing chest pain/)).toBeTruthy();
  });

  it("says to ask for a new code when the link has expired", async () => {
    stubFetch(
      routes(
        {
          error: {
            code: "authentication_failed",
            message: "This code has expired. Please ask the patient to show a new one.",
          },
        },
        401,
      ),
    );
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/stale", path: "/handoff/:token" });

    expect(await screen.findByText(/cannot be opened/i)).toBeTruthy();
    expect(screen.getByText(/show a new one/i)).toBeTruthy();
  });

  it("says what was left out when the code had to trim", async () => {
    stubFetch(routes({ ...VISIT, trimmed: ["ayurvedic findings"] }));
    renderWithProviders(<ScannedVisitPage />, { route: "/handoff/tok", path: "/handoff/:token" });
    expect(await screen.findByText(/not everything is shown/i)).toBeTruthy();
  });
});
