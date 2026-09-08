import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError, api } from "@/services/apiClient";
import { jsonResponse } from "@/test/utils";

/**
 * A free Render instance sleeps after inactivity, and the first request to a
 * sleeping one fails outright while the container starts. The login page
 * loads the demo patients on mount, so that failure was the very first thing
 * a patient saw — reported as "check the connection", blaming their network
 * for our hosting.
 */
describe("reaching a server that is still starting up", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  /** Runs `work` while letting every pending backoff timer elapse. */
  async function settle<T>(work: Promise<T>): Promise<T> {
    const result = work.then(
      (value) => ({ ok: true as const, value }),
      (error) => ({ ok: false as const, error }),
    );
    // Three attempts, so at most two backoffs.
    for (let i = 0; i < 4; i += 1) {
      await vi.advanceTimersByTimeAsync(10_000);
    }
    const settled = await result;
    if (!settled.ok) throw settled.error;
    return settled.value;
  }

  it("retries a GET until the instance answers", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", () => {
      calls += 1;
      if (calls < 3) return Promise.reject(new TypeError("Failed to fetch"));
      return Promise.resolve(jsonResponse([{ demo_key: "standard" }]));
    });

    const result = await settle(api.get<unknown[]>("/auth/demo-patients"));
    expect(result).toEqual([{ demo_key: "standard" }]);
    expect(calls).toBe(3);
  });

  it("gives up with a message that does not blame the patient's connection", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));

    await expect(settle(api.get("/auth/demo-patients"))).rejects.toSatisfy((error: unknown) => {
      const api = error as ApiError;
      expect(api).toBeInstanceOf(ApiError);
      expect(api.code).toBe("network_error");
      expect(api.message).not.toMatch(/check the connection/i);
      expect(api.message).toMatch(/starting up/i);
      return true;
    });
  });

  it("does not retry a server that answered", async () => {
    // A 500 means the server is awake and will say the same thing again.
    let calls = 0;
    vi.stubGlobal("fetch", () => {
      calls += 1;
      return Promise.resolve(
        jsonResponse({ error: { code: "boom", message: "Server error" } }, 500),
      );
    });

    await expect(settle(api.get("/auth/demo-patients"))).rejects.toBeInstanceOf(ApiError);
    expect(calls).toBe(1);
  });

  it("retries asking for a sign-in code, which is safe to repeat", async () => {
    let calls = 0;
    vi.stubGlobal("fetch", () => {
      calls += 1;
      if (calls < 2) return Promise.reject(new TypeError("Failed to fetch"));
      return Promise.resolve(jsonResponse({ mobile_number: "9820011223" }));
    });

    await settle(api.postRetryable("/auth/otp/request", { mobile_number: "9820011223" }));
    expect(calls).toBe(2);
  });

  it("never repeats a document upload", async () => {
    // Retrying could store the same record twice, which a patient would see.
    let calls = 0;
    vi.stubGlobal("fetch", () => {
      calls += 1;
      return Promise.reject(new TypeError("Failed to fetch"));
    });

    await expect(
      settle(api.upload("/patients/me/documents", new FormData())),
    ).rejects.toBeInstanceOf(ApiError);
    expect(calls).toBe(1);
  });
});
