import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, api, localised, tokenStore } from "./apiClient";
import { errorResponse, jsonResponse } from "@/test/utils";

afterEach(() => {
  vi.unstubAllGlobals();
  tokenStore.clear();
});

describe("apiClient", () => {
  it("unwraps the server error envelope into a readable message", async () => {
    vi.stubGlobal("fetch", () =>
      Promise.resolve(errorResponse("Please enter a valid 10-digit Indian mobile number.")),
    );

    await expect(api.post("/auth/otp/request", {})).rejects.toMatchObject({
      status: 422,
      code: "validation_failed",
      message: "Please enter a valid 10-digit Indian mobile number.",
    });
  });

  it("turns a network failure into a patient-readable message", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));

    const error = (await api.get("/patients/me").catch((e: unknown) => e)) as ApiError;
    expect(error).toBeInstanceOf(ApiError);
    expect(error.status).toBe(0);
    expect(error.message).toMatch(/could not reach/i);
    // A network blip is worth retrying; a 422 is not.
    expect(error.isRetryable).toBe(true);
  });

  it("marks 4xx as not retryable and 5xx as retryable", () => {
    expect(new ApiError(422, "x").isRetryable).toBe(false);
    expect(new ApiError(404, "x").isRetryable).toBe(false);
    expect(new ApiError(503, "x").isRetryable).toBe(true);
    expect(new ApiError(401, "x").isUnauthorized).toBe(true);
  });

  it("attaches the bearer token when one is stored", async () => {
    tokenStore.set("abc123");
    const spy = vi.fn((_url: string, _init?: RequestInit) =>
      Promise.resolve(jsonResponse({ ok: true })),
    );
    vi.stubGlobal("fetch", spy);

    await api.get("/patients/me");

    const init = spy.mock.calls[0]![1]!;
    expect((init.headers as Record<string, string>).Authorization).toBe("Bearer abc123");
  });

  it("omits the auth header when signed out", async () => {
    const spy = vi.fn((_url: string, _init?: RequestInit) =>
      Promise.resolve(jsonResponse({ ok: true })),
    );
    vi.stubGlobal("fetch", spy);

    await api.get("/auth/demo-patients");

    const init = spy.mock.calls[0]![1]!;
    expect((init.headers as Record<string, string>).Authorization).toBeUndefined();
  });

  it("does not set a JSON content type for uploads", async () => {
    const spy = vi.fn((_url: string, _init?: RequestInit) =>
      Promise.resolve(jsonResponse({ ok: true })),
    );
    vi.stubGlobal("fetch", spy);

    await api.upload("/patients/me/documents", new FormData());

    const init = spy.mock.calls[0]![1]!;
    expect((init.headers as Record<string, string>)["Content-Type"]).toBeUndefined();
  });

  it("survives a token store that throws", () => {
    const original = window.localStorage.getItem;
    // Private-mode browsers throw on access.
    window.localStorage.getItem = () => {
      throw new Error("denied");
    };
    expect(tokenStore.get()).toBeNull();
    window.localStorage.getItem = original;
  });
});

describe("localised", () => {
  it("returns the active language", () => {
    expect(localised({ en: "Yes", hi: "हाँ" }, "hi")).toBe("हाँ");
  });

  it("falls back to English rather than showing nothing", () => {
    expect(localised({ en: "Yes" }, "hi")).toBe("Yes");
    expect(localised(undefined, "en")).toBe("");
  });
});
