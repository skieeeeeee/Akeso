import { Navigate, useLocation } from "react-router-dom";
import type { ReactNode } from "react";
import { LoadingPanel } from "@/components/ui/States";
import { AppShell } from "@/components/layout/AppShell";
import { useAuth } from "@/providers/AuthProvider";
import { useI18n } from "@/providers/I18nProvider";
import { PROFILE_PATH, canVisit } from "@/features/onboarding/steps";

/** Requires a signed-in patient. */
export function RequireAuth({ children }: { children: ReactNode }) {
  const { status } = useAuth();
  const { t } = useI18n();
  const location = useLocation();

  if (status === "restoring") {
    return (
      <AppShell>
        <LoadingPanel label={t("loading")} />
      </AppShell>
    );
  }
  if (status === "signed_out") {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return <>{children}</>;
}

/**
 * Keeps the URL and the server's recorded progress in agreement: a patient who
 * jumps ahead is sent back to the step they actually reached.
 */
export function RequireStep({ children }: { children: ReactNode }) {
  const { session } = useAuth();
  const location = useLocation();

  if (!session) return <Navigate to="/login" replace />;

  if (!canVisit(session.patient.onboarding_status, location.pathname)) {
    return <Navigate to={session.onboarding.next_route} replace />;
  }
  return <>{children}</>;
}

/** Sends an already-onboarded patient to their profile instead of a step. */
export function RedirectIfComplete({ children }: { children: ReactNode }) {
  const { session } = useAuth();
  if (session?.onboarding.is_complete) return <Navigate to={PROFILE_PATH} replace />;
  return <>{children}</>;
}
