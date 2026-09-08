import { screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { usePreferences } from "./PreferencesProvider";
import { PREFERENCES } from "@/test/fixtures";
import {
  SESSION,
  jsonResponse,
  renderWithProviders,
  route,
  signInForTest,
  stubFetch,
} from "@/test/utils";

function Probe() {
  const { preferences, isEasyMode } = usePreferences();
  return (
    <div>
      <span data-testid="mode">{preferences.interface_mode}</span>
      <span data-testid="easy">{String(isEasyMode)}</span>
      <span data-testid="font">{preferences.font_size}</span>
    </div>
  );
}

function stubPreferences(overrides: Partial<typeof PREFERENCES> = {}) {
  stubFetch([
    route("/auth/me", () => jsonResponse(SESSION)),
    route("/accessibility/preferences", () => jsonResponse({ ...PREFERENCES, ...overrides })),
  ]);
}

beforeEach(() => {
  signInForTest();
  document.documentElement.removeAttribute("data-font-size");
  document.documentElement.removeAttribute("data-contrast");
  document.documentElement.removeAttribute("data-mode");
});

afterEach(() => vi.unstubAllGlobals());

describe("PreferencesProvider", () => {
  it("applies the patient's settings to the document root", async () => {
    stubPreferences({ interface_mode: "easy", font_size: "extra_large", contrast_mode: "high" });
    renderWithProviders(<Probe />);

    await waitFor(() => {
      // Every component inherits accessibility from these attributes.
      expect(document.documentElement.dataset.mode).toBe("easy");
      expect(document.documentElement.dataset.fontSize).toBe("extra_large");
      expect(document.documentElement.dataset.contrast).toBe("high");
    });
  });

  it("exposes easy mode as a flag components can branch on", async () => {
    stubPreferences({ interface_mode: "easy" });
    renderWithProviders(<Probe />);

    await waitFor(() => expect(screen.getByTestId("easy")).toHaveTextContent("true"));
    expect(screen.getByTestId("mode")).toHaveTextContent("easy");
  });

  it("falls back to the plain experience before anything loads", () => {
    // Nothing is assumed about a patient we know nothing about.
    stubFetch([]);
    renderWithProviders(<Probe />);
    expect(screen.getByTestId("mode")).toHaveTextContent("standard");
    expect(screen.getByTestId("font")).toHaveTextContent("normal");
  });

  it("keeps working when the preferences request fails", async () => {
    stubFetch([
      route("/auth/me", () => jsonResponse(SESSION)),
      route("/accessibility/preferences", () =>
        jsonResponse({ error: { code: "database_unavailable", message: "nope" } }, 503),
      ),
    ]);
    renderWithProviders(<Probe />);

    // Degrades to defaults rather than blocking the whole app.
    await waitFor(() => expect(screen.getByTestId("mode")).toHaveTextContent("standard"));
  });
});
