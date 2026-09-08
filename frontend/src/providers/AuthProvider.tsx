import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { ApiError, api, tokenStore } from "@/services/apiClient";
import type { Session } from "@/types/api";

type AuthStatus = "restoring" | "signed_in" | "signed_out";

type AuthValue = {
  status: AuthStatus;
  session: Session | null;
  signIn: (session: Session) => void;
  signOut: () => void;
  /** Re-reads the session so onboarding progress stays accurate. */
  refresh: () => Promise<Session | null>;
};

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [status, setStatus] = useState<AuthStatus>(() =>
    tokenStore.get() ? "restoring" : "signed_out",
  );

  const signIn = useCallback((next: Session) => {
    tokenStore.set(next.access_token);
    setSession(next);
    setStatus("signed_in");
  }, []);

  const signOut = useCallback(() => {
    tokenStore.clear();
    setSession(null);
    setStatus("signed_out");
  }, []);

  const refresh = useCallback(async (): Promise<Session | null> => {
    if (!tokenStore.get()) {
      setStatus("signed_out");
      return null;
    }
    try {
      const next = await api.get<Session>("/auth/me");
      // /auth/me re-issues a token, which keeps a long kiosk session alive.
      tokenStore.set(next.access_token);
      setSession(next);
      setStatus("signed_in");
      return next;
    } catch (error) {
      // An expired or invalid token must not leave the app stuck restoring.
      if (error instanceof ApiError && error.isUnauthorized) {
        tokenStore.clear();
        setSession(null);
        setStatus("signed_out");
        return null;
      }
      // A network problem is not a sign-out; keep whatever we already had.
      setStatus(session ? "signed_in" : "signed_out");
      return null;
    }
  }, [session]);

  // Restore a session once on mount so a refreshed tab stays signed in.
  useEffect(() => {
    if (status !== "restoring") return;
    void refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- run once
  }, []);

  const value = useMemo<AuthValue>(
    () => ({ status, session, signIn, signOut, refresh }),
    [status, session, signIn, signOut, refresh],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}

/** The signed-in patient, or throws — use inside guarded routes only. */
export function useCurrentPatient() {
  const { session } = useAuth();
  if (!session) throw new Error("No signed-in patient");
  return session.patient;
}
