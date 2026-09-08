import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, type RenderResult } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import type { ReactElement, ReactNode } from "react";
import { AuthProvider } from "@/providers/AuthProvider";
import { I18nProvider } from "@/providers/I18nProvider";
import { PreferencesProvider } from "@/providers/PreferencesProvider";
import { tokenStore } from "@/services/apiClient";
import type { Patient, Session } from "@/types/api";

/** A test QueryClient: no retries, no caching between tests. */
export function makeQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0, staleTime: 0 },
      mutations: { retry: false },
    },
  });
}

export function Providers({
  children,
  route = "/",
  path,
  queryClient = makeQueryClient(),
}: {
  children: ReactNode;
  route?: string;
  /** Route pattern to mount under, when the page reads `useParams`. */
  path?: string;
  queryClient?: QueryClient;
}) {
  const tree = path ? (
    <Routes>
      <Route path={path} element={children} />
    </Routes>
  ) : (
    children
  );
  return (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        <I18nProvider>
          <AuthProvider>
            <PreferencesProvider>{tree}</PreferencesProvider>
          </AuthProvider>
        </I18nProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: ReactElement,
  options: { route?: string; path?: string } = {},
): RenderResult {
  return render(
    <Providers route={options.route} path={options.path}>
      {ui}
    </Providers>,
  );
}

// --- Fixtures --------------------------------------------------------------

export const PATIENT: Patient = {
  id: "pat-1",
  full_name: "Priya Menon",
  display_name: "Priya Menon",
  mobile_number: "9812300001",
  date_of_birth: "1988-09-14",
  age: 37,
  gender: "female",
  preferred_language: "en",
  emergency_contact_name: null,
  emergency_contact_number: null,
  emergency_contact_relation: null,
  onboarding_status: "assessment_pending",
  preferred_care_system: null,
  is_demo: false,
  created_at: "2026-01-01T00:00:00Z",
};

export const SESSION: Session = {
  access_token: "test-token",
  token_type: "bearer",
  expires_in_seconds: 3600,
  patient: PATIENT,
  onboarding: {
    status: "assessment_pending",
    step_number: 3,
    total_steps: 6,
    percent: 33,
    next_route: "/onboarding/assessment",
    is_complete: false,
  },
  is_new_patient: false,
};

/** Pretend a patient is already signed in. */
export function signInForTest(): void {
  tokenStore.set(SESSION.access_token);
}

// --- fetch stubbing --------------------------------------------------------

type Responder = (url: string, init?: RequestInit) => Response;
type Route = { match: (url: string, init?: RequestInit) => boolean; respond: Responder };

export function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

export function errorResponse(message: string, status = 422, code = "validation_failed"): Response {
  return jsonResponse({ error: { code, message, details: null } }, status);
}

/**
 * Install a fetch stub. Routes are matched in order; the first match wins, so
 * a test can override a default by registering it first.
 */
export function stubFetch(routes: Route[]): void {
  vi.stubGlobal("fetch", (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === "string" ? input : input.toString();
    const route = routes.find((candidate) => candidate.match(url, init));
    if (!route) {
      return Promise.resolve(jsonResponse({ error: { code: "not_stubbed", message: `No stub for ${url}` } }, 500));
    }
    return Promise.resolve(route.respond(url, init));
  });
}

export function route(
  pattern: string,
  respond: Responder,
  method?: string,
): Route {
  return {
    match: (url, init) =>
      url.includes(pattern) && (!method || (init?.method ?? "GET") === method),
    respond,
  };
}
