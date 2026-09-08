import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ApiError } from "@/services/apiClient";
import { AuthProvider } from "@/providers/AuthProvider";
import { I18nProvider } from "@/providers/I18nProvider";
import { PreferencesProvider } from "@/providers/PreferencesProvider";
import { AppRoutes } from "@/routes/AppRoutes";
import "./index.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // A patient's own data is small; refetching on focus is noise on a kiosk.
      refetchOnWindowFocus: false,
      retry: (failureCount, error) =>
        // Retry only what could plausibly succeed; never retry a 4xx.
        error instanceof ApiError && error.isRetryable && failureCount < 2,
      staleTime: 15_000,
    },
    mutations: { retry: false },
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <I18nProvider>
          <AuthProvider>
            <PreferencesProvider>
              <AppRoutes />
            </PreferencesProvider>
          </AuthProvider>
        </I18nProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
