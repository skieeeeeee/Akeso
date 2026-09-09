import { screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LandingPage } from "./LandingPage";
import { headline, statistics, consultationsInElapsed } from "@/features/landing/statistics";
import { jsonResponse, renderWithProviders, route, stubFetch } from "@/test/utils";

afterEach(() => vi.unstubAllGlobals());

const BASE = [route("/accessibility/preferences", () => jsonResponse({}))];

describe("LandingPage", () => {
  it("leads with the argument for the product", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(
      screen.getByRole("heading", { level: 1, name: /already know your (story|history)/i }),
    ).toBeInTheDocument();
  });

  it("offers log in and register in the nav", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    // Scoped to the nav: a landing page repeats its CTA further down.
    const nav = within(screen.getByRole("banner"));
    expect(nav.getByRole("link", { name: /^log in$/i })).toBeInTheDocument();
    expect(nav.getByRole("link", { name: /^register$/i })).toBeInTheDocument();
  });

  it("routes register and log in into the existing auth flow", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    const nav = within(screen.getByRole("banner"));
    expect(nav.getByRole("link", { name: /^register$/i })).toHaveAttribute("href", "/login");
    expect(nav.getByRole("link", { name: /^log in$/i })).toHaveAttribute("href", "/login");
  });

  it("sends a kiosk visitor to the patient flow", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(screen.getByRole("link", { name: /try the patient flow/i })).toHaveAttribute(
      "href",
      "/start",
    );
  });

  it("shows every statistic with its source and year", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    for (const statistic of [headline(), ...statistics()]) {
      expect(screen.getByText(statistic.label.en)).toBeInTheDocument();
      // An unsourced health number is worse than none, so the citation is
      // rendered with the figure rather than in a footnote.
      expect(
        screen.getAllByText(new RegExp(`${statistic.source}.*${statistic.year}`)).length,
      ).toBeGreaterThan(0);
    }
  });

  it("announces each figure to assistive tech as a complete sentence", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    // The animating digits are aria-hidden; the label carries the value.
    expect(
      screen.getByText(/about 101 million/i, { exact: false }),
    ).toBeInTheDocument();
  });

  it("emphasizes consultation readiness and authentic care focus", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(screen.getByText(/consultation-ready check-in/i)).toBeInTheDocument();
  });

  it("states plainly what the product does not do", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(screen.getByText(/what it does not do/i)).toBeInTheDocument();
    expect(
      screen.getAllByText(/does not diagnose, does not prescribe/i).length,
    ).toBeGreaterThan(0);
  });

  it("says the demo data is fictional and ABHA is simulated", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(screen.getAllByText(/records are fictional/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/not connected to ABDM/i).length).toBeGreaterThan(0);
  });

  it("carries no invented mortality figure", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    const text = document.body.textContent?.toLowerCase() ?? "";
    // There is no measured "deaths from missed check-ups" statistic, so the
    // page must not imply one.
    expect(text).not.toContain("died");
    expect(text).not.toContain("deaths per minute");
    expect(text).not.toContain("dying");
  });

  it("offers a language picker before anything else needs reading", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    const picker = screen.getByRole("combobox");
    expect(picker).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "हिन्दी" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "தமிழ்" })).toBeInTheDocument();
  });

  it("renders in Hindi when Hindi is selected", async () => {
    const user = userEvent.setup();
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    await user.selectOptions(screen.getByRole("combobox"), "hi");
    expect(
      screen.getByRole("heading", { level: 1, name: /आपके डॉक्टर को आपकी कहानी|आपके डॉक्टर को आपका इतिहास/ }),
    ).toBeInTheDocument();
  });

  it("has a skip link and one h1", () => {
    stubFetch(BASE);
    renderWithProviders(<LandingPage />);
    expect(screen.getByRole("link", { name: /skip to main content/i })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
  });
});

describe("ticker arithmetic", () => {
  it("is the elapsed time divided by the cited average", () => {
    expect(consultationsInElapsed(0)).toBe(0);
    expect(consultationsInElapsed(119)).toBe(0);
    expect(consultationsInElapsed(120)).toBe(1);
    expect(consultationsInElapsed(600)).toBe(5);
  });
});
