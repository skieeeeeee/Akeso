import { afterEach, describe, expect, it, vi } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { renderWithProviders } from "@/test/utils";
import { HandoffCode } from "@/features/encounter/HandoffCode";
import { STRINGS } from "@/lib/strings";

const SVG = '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h1v1h-1z"/></svg>';

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("the visit handoff code", () => {
  it("shows the code once it has loaded", async () => {
    vi.stubGlobal("fetch", () => Promise.resolve(new Response(SVG, { status: 200 })));
    renderWithProviders(<HandoffCode encounterId="abc" />);

    const image = await screen.findByRole("img", {
      name: STRINGS.handoffCodeAlt.en,
    });
    expect(image.getAttribute("src")).toMatch(/^data:image\/svg\+xml/);
  });

  it("can be enlarged, because a dense code needs the pixels", async () => {
    vi.stubGlobal("fetch", () => Promise.resolve(new Response(SVG, { status: 200 })));
    renderWithProviders(<HandoffCode encounterId="abc" />);

    await userEvent.click(
      await screen.findByRole("button", { name: new RegExp(STRINGS.handoffEnlarge.en, "i") }),
    );
    expect(screen.getByRole("dialog")).toBeTruthy();

    await userEvent.click(screen.getByRole("button", { name: new RegExp(STRINGS.close.en, "i") }));
    expect(screen.queryByRole("dialog")).toBeNull();
  });

  it("says the answers are safe when the code cannot be made", async () => {
    // Never a bare broken image: the patient has just answered thirty
    // questions and needs to know they were not lost.
    vi.stubGlobal("fetch", () => Promise.resolve(new Response("nope", { status: 500 })));
    renderWithProviders(<HandoffCode encounterId="abc" />);

    await waitFor(() =>
      expect(screen.getByText(STRINGS.handoffFailedBody.en)).toBeTruthy(),
    );
  });

  it("survives the request failing outright", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));
    renderWithProviders(<HandoffCode encounterId="abc" />);

    await waitFor(() =>
      expect(screen.getByText(STRINGS.handoffFailedBody.en)).toBeTruthy(),
    );
  });

  it("sends the token, since a visit is not public", async () => {
    const seen: RequestInit[] = [];
    vi.stubGlobal("fetch", (_url: string, init?: RequestInit) => {
      seen.push(init ?? {});
      return Promise.resolve(new Response(SVG, { status: 200 }));
    });
    renderWithProviders(<HandoffCode encounterId="abc" />);

    await screen.findByRole("img", { name: STRINGS.handoffCodeAlt.en });
    expect(seen).toHaveLength(1);
    expect(seen[0]?.headers).toBeDefined();
  });
});
