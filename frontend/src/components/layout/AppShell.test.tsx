import { describe, expect, it } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { renderWithProviders, stubFetch, jsonResponse, route } from "@/test/utils";
import { LoginPage } from "@/pages/LoginPage";
import { WelcomePage } from "@/pages/WelcomePage";
import { STRINGS } from "@/lib/strings";

describe("shell chrome is not repeated by pages", () => {
  // The footer states the privacy note on every page. Two pages also rendered
  // it inline, so it appeared twice — once as a heading-adjacent reassurance
  // and again in the footer, which reads as a mistake rather than emphasis.
  it.each([
    ["LoginPage", <LoginPage />],
    ["WelcomePage", <WelcomePage />],
  ])("%s states the privacy note exactly once", (_name, element) => {
    stubFetch([route("/auth/demo-patients", () => jsonResponse([]))]);
    renderWithProviders(element);
    expect(screen.getAllByText(STRINGS.privacyNote.en)).toHaveLength(1);
  });
});

describe("the demo patient panel when the list cannot be loaded", () => {
  /**
   * Reported from the deployed site: the panel expanded to an empty box.
   *
   * `data` is undefined on a failed fetch, so the list rendered no rows, and
   * the only empty state was `data?.length === 0` — which is `undefined === 0`,
   * i.e. false. The patient saw a heading, a Hide button, and nothing else.
   */
  it("says so instead of showing an empty box", async () => {
    stubFetch([
      route("/auth/demo-patients", () =>
        jsonResponse({ error: { code: "boom", message: "Server error" } }, 500),
      ),
    ]);
    renderWithProviders(<LoginPage />);

    await userEvent.click(
      screen.getByRole("button", { name: new RegExp(STRINGS.demoShow.en, "i") }),
    );

    const panel = document.getElementById("demo-patient-list");
    expect(panel).not.toBeNull();
    await waitFor(() => expect(panel!.textContent?.trim()).not.toBe(""));
    // And it offers a way out rather than a dead end.
    expect(
      screen.getByRole("button", { name: new RegExp(STRINGS.retry.en, "i") }),
    ).toBeTruthy();
  });
});
