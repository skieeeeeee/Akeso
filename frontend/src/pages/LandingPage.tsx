import {
  Accessibility,
  ArrowRight,
  BookOpenCheck,
  Building2,
  Clock,
  Database,
  FileScan,
  HeartPulse,
  Languages,
  Menu,
  Mic,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  Wrench,
  X,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { cn } from "@/lib/cn";
import { LANGUAGE_LABELS, useI18n } from "@/providers/I18nProvider";
import { useAuth } from "@/providers/AuthProvider";
import { StatCounter } from "@/features/landing/StatCounter";
import { FIGURES_COMPILED, HEADLINE, STATISTICS } from "@/features/landing/statistics";
import { postLoginRoute } from "@/features/onboarding/steps";
import type { Language } from "@/types/api";

/**
 * The public landing page.
 *
 * Its own chrome rather than `AppShell`, because this is the marketing
 * surface: it needs a nav with authentication rather than the kiosk's
 * accessibility bar. It shares the design system so the two do not feel
 * like different products.
 */
export function LandingPage() {
  const { t, language, setLanguage, supported } = useI18n();
  const { session } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const signedInRoute = session
    ? postLoginRoute(session.onboarding.next_route, session.onboarding.is_complete)
    : "/login";

  const NAV = [
    { href: "#how-it-works", label: t("navHowItWorks") },
    { href: "#features", label: t("navFeatures") },
    { href: "#specifications", label: t("landingSpecsTitle") },
    { href: "#for-clinics", label: t("navForClinics") },
  ];

  const FEATURES = [
    { icon: Mic, title: t("featVoiceTitle"), body: t("featVoiceBody") },
    { icon: Accessibility, title: t("featAccessTitle"), body: t("featAccessBody") },
    { icon: FileScan, title: t("featOcrTitle"), body: t("featOcrBody") },
    { icon: ShieldAlert, title: t("featSafetyTitle"), body: t("featSafetyBody") },
    { icon: BookOpenCheck, title: t("featAyushTitle"), body: t("featAyushBody") },
    { icon: ShieldCheck, title: t("featConsentTitle"), body: t("featConsentBody") },
  ];

  const STEPS = [
    { title: t("landingHow1"), body: t("landingHow1Body") },
    { title: t("landingHow2"), body: t("landingHow2Body") },
    { title: t("landingHow3"), body: t("landingHow3Body") },
  ];

  const SPECS = [
    { icon: Wrench, title: t("specStack"), body: t("specStackBody") },
    { icon: Database, title: t("specData"), body: t("specDataBody") },
    { icon: Sparkles, title: t("specAi"), body: t("specAiBody") },
    { icon: Languages, title: t("specLanguages"), body: t("specLanguagesBody") },
    { icon: ShieldCheck, title: t("specFailure"), body: t("specFailureBody") },
    { icon: Accessibility, title: t("specAccess"), body: t("specAccessBody") },
  ];

  return (
    <div className="flex min-h-screen flex-col">
      <a
        href="#main"
        className="sr-only-focusable z-50 m-2 rounded-lg bg-primary px-4 py-2 font-semibold text-white"
      >
        {t("skipToContent")}
      </a>

      {/* ---------- Nav ---------- */}
      <header className="sticky top-0 z-40 border-b border-line bg-surface/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Link to="/" className="flex items-center gap-3 rounded-xl">
            <span
              aria-hidden="true"
              className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-white"
            >
              <HeartPulse className="h-6 w-6" />
            </span>
            <span>
              <span className="block text-lg font-bold leading-none text-ink">
                {t("appName")}
              </span>
              <span className="mt-1 hidden text-xs text-ink-muted sm:block">
                {t("appTagline")}
              </span>
            </span>
          </Link>

          <nav aria-label={t("navFeatures")} className="hidden items-center gap-1 lg:flex">
            {NAV.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="rounded-lg px-3 py-2 text-sm font-semibold text-ink-muted hover:bg-surface-muted hover:text-ink"
              >
                {item.label}
              </a>
            ))}
          </nav>

          <div className="flex items-center gap-2">
            {/* Language is in the nav because a visitor may not read English. */}
            <label className="relative hidden min-h-touch items-center gap-1.5 rounded-xl px-2 text-ink-muted hover:bg-surface-muted sm:inline-flex">
              <Languages className="h-5 w-5" aria-hidden="true" />
              <span className="sr-only">{t("chooseLanguage")}</span>
              <select
                value={language}
                onChange={(event) => setLanguage(event.target.value as Language)}
                className="cursor-pointer appearance-none bg-transparent py-2 text-sm font-semibold text-ink focus:outline-none"
              >
                {supported.map((code) => (
                  <option key={code} value={code}>
                    {LANGUAGE_LABELS[code].native}
                  </option>
                ))}
              </select>
            </label>

            <Button variant="ghost" size="md" asChild className="hidden sm:inline-flex">
              <Link to={signedInRoute}>{session ? t("continue") : t("navLogIn")}</Link>
            </Button>
            <Button size="md" asChild>
              <Link to="/login">{session ? t("navKiosk") : t("navRegister")}</Link>
            </Button>

            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              aria-expanded={menuOpen}
              aria-label={t("navFeatures")}
              onClick={() => setMenuOpen((open) => !open)}
            >
              {menuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {menuOpen && (
          <nav className="border-t border-line bg-surface px-4 py-2 lg:hidden" aria-label={t("navFeatures")}>
            {NAV.map((item) => (
              <a
                key={item.href}
                href={item.href}
                onClick={() => setMenuOpen(false)}
                className="block min-h-touch rounded-lg px-3 py-3 text-base font-semibold text-ink-muted hover:bg-surface-muted"
              >
                {item.label}
              </a>
            ))}
          </nav>
        )}
      </header>

      <main id="main" className="flex-1">
        {/* ---------- Hero ---------- */}
        <section className="border-b border-line bg-surface">
          <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:px-6 sm:py-16 lg:grid-cols-[1.15fr_1fr] lg:items-center">
            <div className="space-y-6">
              <h1 className="text-3xl font-bold leading-tight text-ink sm:text-4xl lg:text-5xl">
                {t("landingHeadline")}
              </h1>
              <p className="max-w-2xl text-lg text-ink-muted">{t("landingSubhead")}</p>

              <div className="flex flex-col gap-3 sm:flex-row">
                <Button size="xl" asChild>
                  <Link to="/start">
                    {t("landingPrimaryCta")}
                    <ArrowRight className="h-6 w-6" aria-hidden="true" />
                  </Link>
                </Button>
                <Button size="xl" variant="secondary" asChild>
                  <Link to="/login">{t("landingSecondaryCta")}</Link>
                </Button>
              </div>

              <p className="text-sm text-ink-subtle">{t("landingPrototypeNote")}</p>
            </div>

            {/* The headline statistic & consultation readiness */}
            <Card className="bg-surface-muted shadow-sm">
              <CardBody className="space-y-5">
                <StatCounter statistic={HEADLINE} />
                <div className="rounded-2xl border-2 border-primary/25 bg-primary-soft px-5 py-4">
                  <p className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-primary-ink">
                    <Clock className="h-4 w-4" aria-hidden="true" />
                    {t("consultationReadyTitle")}
                  </p>
                  <p className="mt-2 text-base text-primary-ink leading-relaxed">
                    {t("consultationReadyBody")}
                  </p>
                </div>
              </CardBody>
            </Card>
          </div>
        </section>

        {/* ---------- Problem + statistics ---------- */}
        <section className="border-b border-line" aria-labelledby="why">
          <div className="mx-auto max-w-6xl space-y-8 px-4 py-12 sm:px-6 sm:py-16">
            <div className="max-w-3xl space-y-3">
              <h2 id="why" className="text-2xl font-bold text-ink sm:text-3xl">
                {t("landingProblemTitle")}
              </h2>
              <p className="text-lg text-ink-muted">{t("landingProblemBody")}</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-ink">{t("landingStatsTitle")}</h3>
              <div className="mt-4 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {STATISTICS.map((statistic) => (
                  <Card key={statistic.id}>
                    <CardBody>
                      <StatCounter statistic={statistic} />
                    </CardBody>
                  </Card>
                ))}
              </div>
              {/* Honest about provenance rather than implying live data. */}
              <p className="mt-4 text-xs text-ink-subtle">
                {t("landingStatsNote")} ({FIGURES_COMPILED})
              </p>
            </div>
          </div>
        </section>

        {/* ---------- How it works ---------- */}
        <section id="how-it-works" className="border-b border-line bg-surface" aria-labelledby="how">
          <div className="mx-auto max-w-6xl space-y-8 px-4 py-12 sm:px-6 sm:py-16">
            <h2 id="how" className="text-2xl font-bold text-ink sm:text-3xl">
              {t("landingHowTitle")}
            </h2>

            <ol className="grid gap-4 lg:grid-cols-3">
              {STEPS.map((step, index) => (
                <li key={step.title}>
                  <Card className="h-full">
                    <CardBody className="space-y-3">
                      <span
                        aria-hidden="true"
                        className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-base font-bold text-white"
                      >
                        {index + 1}
                      </span>
                      <h3 className="text-lg font-semibold text-ink">{step.title}</h3>
                      <p className="text-base text-ink-muted">{step.body}</p>
                    </CardBody>
                  </Card>
                </li>
              ))}
            </ol>

            <Card className="border-primary/30 bg-primary-soft">
              <CardBody className="flex items-start gap-4">
                <Stethoscope className="mt-0.5 h-6 w-6 shrink-0 text-primary" aria-hidden="true" />
                <div>
                  <h3 className="text-lg font-semibold text-primary-ink">
                    {t("landingReturningTitle")}
                  </h3>
                  <p className="mt-1 text-base text-primary-ink/90">
                    {t("landingReturningBody")}
                  </p>
                </div>
              </CardBody>
            </Card>
          </div>
        </section>

        {/* ---------- Features ---------- */}
        <section id="features" className="border-b border-line" aria-labelledby="features-heading">
          <div className="mx-auto max-w-6xl space-y-8 px-4 py-12 sm:px-6 sm:py-16">
            <h2 id="features-heading" className="text-2xl font-bold text-ink sm:text-3xl">
              {t("landingFeaturesTitle")}
            </h2>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {FEATURES.map(({ icon: Icon, title, body }) => (
                <Card key={title} className="h-full">
                  <CardBody className="space-y-3">
                    <span
                      aria-hidden="true"
                      className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary-soft text-primary"
                    >
                      <Icon className="h-5 w-5" />
                    </span>
                    <h3 className="text-lg font-semibold text-ink">{title}</h3>
                    <p className="text-base text-ink-muted">{body}</p>
                  </CardBody>
                </Card>
              ))}
            </div>

            {/* Stated as prominently as the features themselves. */}
            <Alert tone="info" title={t("landingSafetyTitle")}>
              <p className="text-base">{t("landingSafetyBody")}</p>
            </Alert>
          </div>
        </section>

        {/* ---------- Specifications ---------- */}
        <section id="specifications" className="border-b border-line bg-surface" aria-labelledby="specs">
          <div className="mx-auto max-w-6xl space-y-8 px-4 py-12 sm:px-6 sm:py-16">
            <h2 id="specs" className="text-2xl font-bold text-ink sm:text-3xl">
              {t("landingSpecsTitle")}
            </h2>
            <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {SPECS.map(({ icon: Icon, title, body }) => (
                <div key={title} className="rounded-2xl border border-line bg-surface-muted p-5">
                  <dt className="flex items-center gap-2 text-base font-semibold text-ink">
                    <Icon className="h-5 w-5 text-primary" aria-hidden="true" />
                    {title}
                  </dt>
                  <dd className="mt-2 text-sm text-ink-muted">{body}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* ---------- For clinics + closing CTA ---------- */}
        <section id="for-clinics" aria-labelledby="clinics">
          <div className="mx-auto grid max-w-6xl gap-6 px-4 py-12 sm:px-6 sm:py-16 lg:grid-cols-2">
            <Card>
              <CardBody className="space-y-3">
                <span
                  aria-hidden="true"
                  className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary-soft text-primary"
                >
                  <Building2 className="h-5 w-5" />
                </span>
                <h2 id="clinics" className="text-xl font-bold text-ink">
                  {t("landingClinicTitle")}
                </h2>
                <p className="text-base text-ink-muted">{t("landingClinicBody")}</p>
              </CardBody>
            </Card>

            <Card className="border-primary/30 bg-primary-soft">
              <CardBody className="space-y-4">
                <h2 className="text-xl font-bold text-primary-ink">
                  {t("landingClosingTitle")}
                </h2>
                <p className="text-base text-primary-ink/90">{t("landingClosingBody")}</p>
                <div className="flex flex-col gap-3 sm:flex-row">
                  <Button size="lg" asChild>
                    <Link to="/login">{t("navRegister")}</Link>
                  </Button>
                  <Button size="lg" variant="secondary" asChild>
                    <Link to="/start">{t("navKiosk")}</Link>
                  </Button>
                </div>
              </CardBody>
            </Card>
          </div>
        </section>
      </main>

      <footer className="border-t border-line bg-surface">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-6 text-sm text-ink-subtle sm:px-6">
          <p className={cn("font-semibold text-ink-muted")}>{t("appName")}</p>
          <p>{t("landingSafetyBody")}</p>
          <p>{t("landingPrototypeNote")}</p>
        </div>
      </footer>
    </div>
  );
}
