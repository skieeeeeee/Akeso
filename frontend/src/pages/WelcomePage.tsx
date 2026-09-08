import { Link, useNavigate } from "react-router-dom";
import { ArrowRight, ClipboardList, MessageSquareHeart, ShieldCheck, Smartphone } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { OptionCard, OptionGrid } from "@/components/ui/OptionCard";
import { LANGUAGE_LABELS, useI18n } from "@/providers/I18nProvider";
import { useAuth } from "@/providers/AuthProvider";
import { usePreferences } from "@/providers/PreferencesProvider";
import { postLoginRoute } from "@/features/onboarding/steps";
import type { Language } from "@/types/api";

const HOW_IT_WORKS = [
  { icon: Smartphone, title: "step1Title", body: "step1Body" },
  { icon: MessageSquareHeart, title: "step2Title", body: "step2Body" },
  { icon: ClipboardList, title: "step3Title", body: "step3Body" },
] as const;

export function WelcomePage() {
  const { t, language, setLanguage, supported } = useI18n();
  const { session } = useAuth();
  const { isEasyMode } = usePreferences();
  const navigate = useNavigate();

  const start = () =>
    navigate(
      session
        ? postLoginRoute(session.onboarding.next_route, session.onboarding.is_complete)
        : "/login",
    );

  return (
    <AppShell>
      <div className="space-y-6">
        <Card>
          <CardBody className="space-y-6 py-8 sm:py-10">
            <div className="space-y-3 text-center">
              <h1 className={isEasyMode ? "text-4xl font-bold leading-tight" : "text-3xl font-bold leading-tight sm:text-4xl"}>
                {t("welcomeHeading")}
              </h1>
              <p className="mx-auto max-w-2xl text-lg text-ink-muted">{t("welcomeBody")}</p>
            </div>

            {/* Language first: a patient must be able to read the rest. */}
            <fieldset className="mx-auto max-w-form space-y-3">
              <legend className="mb-1 block text-center text-base font-semibold text-ink">
                {t("chooseLanguage")}
              </legend>
              <OptionGrid columns={2}>
                {supported.map((code) => (
                  <OptionCard
                    key={code}
                    name="language"
                    value={code}
                    checked={language === code}
                    onSelect={(value) => setLanguage(value as Language)}
                    label={LANGUAGE_LABELS[code].native}
                    help={code === language ? undefined : LANGUAGE_LABELS[code].english}
                  />
                ))}
              </OptionGrid>
            </fieldset>

            <div className="flex flex-col items-center gap-3">
              <Button size="xl" onClick={start} className="w-full max-w-form">
                {session ? t("continue") : t("welcomeStart")}
                <ArrowRight className="h-6 w-6" aria-hidden="true" />
              </Button>
              {!session && (
                <Button variant="ghost" size="md" asChild>
                  <Link to="/login">{t("welcomeReturning")}</Link>
                </Button>
              )}
            </div>
          </CardBody>
        </Card>

        {/* Purposeful supporting content — the screen is never an empty hero. */}
        <section aria-labelledby="how-it-works" className="space-y-3">
          <h2 id="how-it-works" className="text-lg font-semibold text-ink">
            {t("howItWorks")}
          </h2>
          <div className="grid gap-3 sm:grid-cols-3">
            {HOW_IT_WORKS.map(({ icon: Icon, title, body }, index) => (
              <Card key={title}>
                <CardBody className="space-y-2">
                  <div className="flex items-center gap-3">
                    <span
                      aria-hidden="true"
                      className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-soft text-primary"
                    >
                      <Icon className="h-5 w-5" />
                    </span>
                    <span className="text-sm font-bold text-ink-subtle">{index + 1}</span>
                  </div>
                  <p className="font-semibold text-ink">{t(title)}</p>
                  <p className="text-sm text-ink-muted">{t(body)}</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>

        <Card className="border-primary/25 bg-primary-soft">
          <CardBody className="flex items-start gap-3">
            <ShieldCheck className="mt-0.5 h-6 w-6 shrink-0 text-primary" aria-hidden="true" />
            <p className="text-base text-primary-ink">{t("welcomeConsent")}</p>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
