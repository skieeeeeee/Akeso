import { describe, expect, it } from "vitest";
import { screen } from "@testing-library/react";
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
