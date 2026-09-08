import {
  ArrowLeft,
  CalendarClock,
  FileText,
  HeartPulse,
  Home,
  LogOut,
  Settings2,
  UserRound,
} from "lucide-react";
import type { ReactNode } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { cn } from "@/lib/cn";
import { useAuth } from "@/providers/AuthProvider";
import { useI18n } from "@/providers/I18nProvider";
import { Button } from "@/components/ui/Button";
import { AccessibilityBar } from "./AccessibilityBar";

/** The frame every screen sits in: header, skip link, main landmark, footer. */
export function AppShell({
  children,
  headerRight,
  wide,
  backRoute,
  backLabel,
  showNav = true,
}: {
  children: ReactNode;
  headerRight?: ReactNode;
  wide?: boolean;
  backRoute?: string;
  backLabel?: string;
  showNav?: boolean;
}) {
  const { t } = useI18n();
  const { status, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const isSignedIn = status === "signed_in";

  const homeTarget = isSignedIn ? "/home" : "/";
  const isOnboarding = location.pathname.startsWith("/onboarding");
  const isVisitFlow = location.pathname.startsWith("/visit");
  const shouldRenderNav = isSignedIn && showNav && !isOnboarding && !isVisitFlow;

  const NAV_ITEMS = [
    { to: "/home", label: t("navHome"), icon: Home },
    { to: "/records", label: t("navRecords"), icon: FileText },
    { to: "/timeline", label: t("navTimeline"), icon: CalendarClock },
    { to: "/profile", label: t("navProfile"), icon: UserRound },
    { to: "/settings", label: t("navSettings"), icon: Settings2 },
  ];

  return (
    <div className="flex min-h-screen flex-col bg-canvas text-ink">
      <a
        href="#main"
        className="sr-only-focusable z-50 m-2 rounded-lg bg-primary px-4 py-2 font-semibold text-white"
      >
        {t("skipToContent")}
      </a>

      <header className="sticky top-0 z-30 border-b border-line bg-surface/95 backdrop-blur">
        <div
          className={cn(
            "mx-auto flex flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6",
            wide ? "max-w-6xl" : "max-w-kiosk",
          )}
        >
          {/* Logo is always a link to Home */}
          <div className="flex items-center gap-3">
            <Link
              to={homeTarget}
              className="group flex items-center gap-3 rounded-xl transition-opacity hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
              aria-label={`${t("appName")} - ${t("navHome")}`}
            >
              <span
                aria-hidden="true"
                className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-white shadow-sm transition-transform group-hover:scale-105"
              >
                <HeartPulse className="h-6 w-6" />
              </span>
              <div>
                <p className="text-lg font-bold leading-none text-ink">{t("appName")}</p>
                <p className="mt-1 text-xs text-ink-muted sm:text-sm">{t("appTagline")}</p>
              </div>
            </Link>
          </div>

          {/* Desktop Patient Navigation */}
          {shouldRenderNav && (
            <nav
              aria-label={t("appName")}
              className="hidden items-center gap-1 md:flex"
            >
              {NAV_ITEMS.map((item) => {
                const Icon = item.icon;
                const isActive =
                  location.pathname === item.to ||
                  (item.to !== "/home" && location.pathname.startsWith(item.to));
                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    className={cn(
                      "flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-semibold transition-colors",
                      isActive
                        ? "bg-primary-soft text-primary-ink font-bold"
                        : "text-ink-muted hover:bg-surface-muted hover:text-ink",
                    )}
                  >
                    <Icon className="h-4 w-4" aria-hidden="true" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          )}

          <div className="flex items-center gap-2">
            {headerRight}
            <AccessibilityBar />
            {/* Available on every signed-in screen: this runs on shared
                kiosks, so ending the session must never require navigating
                somewhere else first. */}
            {isSignedIn && (
              <Button
                variant="ghost"
                size="md"
                onClick={() => {
                  signOut();
                  navigate("/");
                }}
              >
                <LogOut className="h-5 w-5" aria-hidden="true" />
                <span className="hidden sm:inline">{t("signOut")}</span>
              </Button>
            )}
          </div>
        </div>

        {/* Mobile Navigation bar for signed-in patients */}
        {shouldRenderNav && (
          <nav
            aria-label={t("appName")}
            className="flex border-t border-line bg-surface px-2 py-1 md:hidden overflow-x-auto justify-around"
          >
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive =
                location.pathname === item.to ||
                (item.to !== "/home" && location.pathname.startsWith(item.to));
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={cn(
                    "flex flex-col items-center gap-0.5 rounded-lg px-2.5 py-1 text-xs font-semibold transition-colors",
                    isActive
                      ? "text-primary"
                      : "text-ink-muted hover:text-ink",
                  )}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        )}
      </header>

      <main
        id="main"
        className={cn(
          "mx-auto w-full flex-1 px-4 py-6 sm:px-6 sm:py-8",
          wide ? "max-w-6xl" : "max-w-kiosk",
        )}
      >
        {backRoute && (
          <div className="mb-4">
            <Link
              to={backRoute}
              className="inline-flex items-center gap-1.5 rounded-lg border border-line bg-surface px-3 py-1.5 text-sm font-semibold text-ink-muted transition-colors hover:border-primary hover:text-ink shadow-sm"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              {backLabel ?? t("backToHome")}
            </Link>
          </div>
        )}
        {children}
      </main>

      <footer className="border-t border-line bg-surface">
        <div
          className={cn(
            "mx-auto px-4 py-4 text-center text-xs text-ink-subtle sm:px-6",
            wide ? "max-w-6xl" : "max-w-kiosk",
          )}
        >
          {t("privacyNote")}
        </div>
      </footer>
    </div>
  );
}
