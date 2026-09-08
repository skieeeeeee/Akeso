/**
 * The single HTTP client.
 *
 * Everything the app knows about talking to the server lives here: the auth
 * header, the `{error:{code,message}}` envelope, and turning failures into a
 * typed `ApiError` carrying a message that is already safe to show a patient.
 */
import type { Language } from "@/types/api";

/**
 * Where the API lives.
 *
 * Empty by default, which keeps every request same-origin: the dev server
 * proxies `/api`, and a single-origin deployment needs nothing else. Set
 * `VITE_API_BASE_URL` at build time to point the client at a separately
 * hosted API — the frontend on Vercel and the API on Render, say — in which
 * case that origin must also list this one in `CORS_ORIGINS`.
 *
 * A trailing slash is stripped so both forms of the variable work.
 */
const ORIGIN = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/+$/, "");
const BASE = `${ORIGIN}/api/v1`;
const TOKEN_KEY = "medikiosk.token";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
    readonly code: string = "error",
    readonly details: unknown = null,
  ) {
    super(message);
    this.name = "ApiError";
  }

  /** True when retrying could plausibly succeed. */
  get isRetryable(): boolean {
    return this.status === 0 || this.status >= 500;
  }

  get isUnauthorized(): boolean {
    return this.status === 401;
  }
}

// --- Token storage ---------------------------------------------------------
// Kept in localStorage so a refreshed kiosk tab does not lose the session.
// Reads and writes are guarded because private-mode browsers can throw.

export const tokenStore = {
  get(): string | null {
    try {
      return window.localStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },
  set(token: string): void {
    try {
      window.localStorage.setItem(TOKEN_KEY, token);
    } catch {
      /* session simply will not survive a reload */
    }
  },
  clear(): void {
    try {
      window.localStorage.removeItem(TOKEN_KEY);
    } catch {
      /* nothing to do */
    }
  },
};

type RequestOptions = {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE";
  body?: unknown;
  /** Set for multipart uploads, where the browser must set the boundary. */
  formData?: FormData;
  signal?: AbortSignal;
};

const NETWORK_MESSAGE =
  "We could not reach the MediKiosk server. Check the connection and try again.";

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const token = tokenStore.get();
  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (!options.formData && options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }

  let response: Response;
  try {
    response = await fetch(`${BASE}${path}`, {
      method: options.method ?? "GET",
      headers,
      body: options.formData ?? (options.body !== undefined ? JSON.stringify(options.body) : undefined),
      signal: options.signal,
    });
  } catch {
    throw new ApiError(0, NETWORK_MESSAGE, "network_error");
  }

  if (response.status === 204) return undefined as T;

  const text = await response.text();
  const payload = text ? safeParse(text) : null;

  if (!response.ok) {
    const envelope = (payload as { error?: { code?: string; message?: string; details?: unknown } } | null)?.error;
    throw new ApiError(
      response.status,
      envelope?.message ?? `Something went wrong (${response.status}).`,
      envelope?.code ?? "error",
      envelope?.details ?? null,
    );
  }
  return payload as T;
}

function safeParse(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

/**
 * Where the API lives, and the auth header for it.
 *
 * Exposed for the few calls that cannot go through `api.*` because they do
 * not return JSON — speech synthesis returns audio bytes. Everything else
 * should use the helpers below.
 */
export const apiBase = BASE;

export function authHeaders(): Record<string, string> {
  const token = tokenStore.get();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export const api = {
  get: <T>(path: string, signal?: AbortSignal) => request<T>(path, { signal }),
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: "POST", body: body ?? {} }),
  patch: <T>(path: string, body: unknown) => request<T>(path, { method: "PATCH", body }),
  put: <T>(path: string, body: unknown) => request<T>(path, { method: "PUT", body }),
  del: <T>(path: string) => request<T>(path, { method: "DELETE" }),
  upload: <T>(path: string, formData: FormData) => request<T>(path, { method: "POST", formData }),
};

/**
 * Fallback chain, mirroring `app/shared/i18n.py`.
 *
 * Marathi is written in Devanagari, and Hindi is widely read in Maharashtra,
 * Gujarat and Punjab — so Hindi is a genuine second choice for those three.
 * Tamil is the exception: Devanagari is not read in Tamil Nadu, so Hindi
 * would be no more useful to a Tamil patient than a blank, and English at
 * least shares a script with the signage and prescriptions around them.
 */
const FALLBACK_CHAIN: Record<Language, Language[]> = {
  en: ["en"],
  hi: ["hi", "en"],
  mr: ["mr", "hi", "en"],
  gu: ["gu", "hi", "en"],
  pa: ["pa", "hi", "en"],
  ta: ["ta", "en"],
};

/** Resolve a localised value for the active language, never returning undefined. */
export function localised(
  value: Partial<Record<string, string>> | undefined,
  language: Language,
): string {
  if (!value) return "";
  for (const candidate of FALLBACK_CHAIN[language] ?? ["en"]) {
    const text = value[candidate];
    if (text) return text;
  }
  // Last resort: any translation beats an empty screen.
  return Object.values(value).find((text) => Boolean(text)) ?? "";
}
