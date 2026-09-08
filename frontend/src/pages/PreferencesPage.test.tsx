import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { PreferencesPage } from "./PreferencesPage";
import { ASSESSMENT_CONTENT, PREFERENCES } from "@/test/fixtures";
import {
  SESSION,
  jsonResponse,
  renderWithProviders,
  route,
  signInForTest,
  stubFetch,
} from "@/test/utils";

const RECOMMENDATION = {
  interface_mode: "easy",
  font_size: "large",
  contrast_mode: "normal",
  audio_guidance: true,
  interaction_preference: "voice",
  language: "en",
  easy_mode_score: 4,
  easy_mode_threshold: 3,
  reasons: [
    {
      code: "easy_mode_digital_comfort",
      en: "You told us you prefer a simpler experience.",
      hi: "आपने बताया कि आपको आसान अनुभव पसंद है।",
    },
  ],
};

function stubPage(extra: ReturnType<typeof route>[] = []) {
  stubFetch([
    ...extra,
    route("/auth/me", () => jsonResponse(SESSION)),
    route("/accessibility/recommendation", () => jsonResponse(RECOMMENDATION)),
    route("/accessibility/content", () => jsonResponse(ASSESSMENT_CONTENT)),
    route("/accessibility/preferences", () =>
      jsonResponse({ ...PREFERENCES, interface_mode: "easy", font_size: "large", audio_guidance: true }),
    ),
  ]);
}

beforeEach(signInForTest);
afterEach(() => vi.unstubAllGlobals());

describe("PreferencesPage", () => {
  it("shows the recommendation with the reasons behind it", async () => {
    stubPage();
    renderWithProviders(<PreferencesPage />);

    expect(await screen.findByText(RECOMMENDATION.reasons[0]!.en)).toBeInTheDocument();
    // The chosen settings are summarised, not hidden behind a form.
    expect(await screen.findByText(/^Easy$/)).toBeInTheDocument();
    expect(await screen.findByText(/^Large$/)).toBeInTheDocument();
  });

  it("accepts the recommendation as recommended", async () => {
    const user = userEvent.setup();
    const save = vi.fn((_url: string, _init?: RequestInit) => jsonResponse(PREFERENCES));
    stubPage([route("/accessibility/preferences", save, "PUT")]);
    renderWithProviders(<PreferencesPage />);

    await user.click(await screen.findByRole("button", { name: /this looks good/i }));

    await waitFor(() => expect(save).toHaveBeenCalled());
    const body = JSON.parse(save.mock.calls[0]![1]!.body as string);
    expect(body.accepted_recommendation).toBe(true);
  });

  it("lets the patient switch out of easy mode and records it as customised", async () => {
    const user = userEvent.setup();
    const save = vi.fn((_url: string, _init?: RequestInit) =>
      jsonResponse({ ...PREFERENCES, source: "customized" }),
    );
    stubPage([route("/accessibility/preferences", save, "PUT")]);
    renderWithProviders(<PreferencesPage />);

    await user.click(await screen.findByRole("button", { name: /change these settings/i }));

    // The customise view exposes the mode choices.
    const standard = await screen.findByRole("radio", { name: /standard/i });
    await user.click(standard);

    // Changing a setting applies immediately, so the effect is visible.
    await waitFor(() => expect(document.documentElement.dataset.mode).toBe("standard"));

    await user.click(screen.getByRole("button", { name: /^save$/i }));
    await waitFor(() => expect(save).toHaveBeenCalled());
    const body = JSON.parse(save.mock.calls.at(-1)![1]!.body as string);
    expect(body.accepted_recommendation).toBe(false);
    expect(body.interface_mode).toBe("standard");
  });

  it("previews a text-size change straight away", async () => {
    const user = userEvent.setup();
    stubPage();
    renderWithProviders(<PreferencesPage />);

    await user.click(await screen.findByRole("button", { name: /change these settings/i }));
    await user.click(await screen.findByRole("radio", { name: /extra large/i }));

    await waitFor(() => expect(document.documentElement.dataset.fontSize).toBe("extra_large"));
  });

  it("tells the patient they are not locked in", async () => {
    stubPage();
    renderWithProviders(<PreferencesPage />);
    expect(await screen.findByText(/never locked into a setting/i)).toBeInTheDocument();
  });
});
