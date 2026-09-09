import { beforeEach, describe, expect, it } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { renderWithProviders } from "@/test/utils";
import { useI18n } from "@/providers/I18nProvider";
import { STRINGS } from "@/lib/strings";
import { GUJARATI } from "@/lib/translations/gu";
import { TAMIL } from "@/lib/translations/ta";

// `continue` carries only English and Hindi inline; the regional text lives
// in the overlay files, which is exactly what these tests are about.
const EXPECTED = {
  ta: TAMIL[STRINGS.continue.en],
  gu: GUJARATI[STRINGS.continue.en],
};

/**
 * The regional translation files are fetched on demand rather than shipped to
 * every patient, which took 41% off the first download. The risk that buys is
 * a render that happens before the file arrives.
 */

function Probe() {
  const { t, language, setLanguage } = useI18n();
  return (
    <div>
      <p data-testid="lang">{language}</p>
      <p data-testid="copy">{t("continue")}</p>
      <button type="button" onClick={() => setLanguage("gu")}>
        switch
      </button>
    </div>
  );
}

beforeEach(() => {
  window.localStorage.clear();
});

describe("translations that load on demand", () => {
  it("reaches the screen once the file arrives", async () => {
    // The bug this guards: the context value was memoised on the language
    // alone, so when the overlay landed every consumer received a
    // referentially identical value and never re-rendered. Tamil showed 168
    // characters of Tamil on the landing page instead of 5,214.
    window.localStorage.setItem("medikiosk.language", "ta");
    renderWithProviders(<Probe />);

    await waitFor(() =>
      expect(screen.getByTestId("copy").textContent).toBe(EXPECTED.ta),
    );
  });

  it("does not get stuck in the fallback language", async () => {
    window.localStorage.setItem("medikiosk.language", "gu");
    renderWithProviders(<Probe />);

    await waitFor(() =>
      expect(screen.getByTestId("copy").textContent).toBe(EXPECTED.gu),
    );
    // Gujarati falls back to Hindi, which is exactly what it looked like
    // while the bug was present.
    expect(screen.getByTestId("copy").textContent).not.toBe(STRINGS.continue.hi);
  });

  it("switches language with the text already in hand", async () => {
    window.localStorage.setItem("medikiosk.language", "en");
    renderWithProviders(<Probe />);
    expect(screen.getByTestId("copy").textContent).toBe(STRINGS.continue.en);

    await userEvent.click(screen.getByRole("button", { name: "switch" }));

    await waitFor(() => expect(screen.getByTestId("lang").textContent).toBe("gu"));
    // The switch waits for the file, so there is no frame of the fallback.
    expect(screen.getByTestId("copy").textContent).toBe(EXPECTED.gu);
  });

  it("needs no extra fetch for English or Hindi, which are inline", async () => {
    window.localStorage.setItem("medikiosk.language", "hi");
    renderWithProviders(<Probe />);
    // Available on the very first render, with nothing awaited.
    expect(screen.getByTestId("copy").textContent).toBe(STRINGS.continue.hi);
  });
});
