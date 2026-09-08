import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  KeyRound,
  Phone,
  ShieldCheck,
  Sparkles,
  TestTube2,
  Volume2,
} from "lucide-react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { Field, Input } from "@/components/ui/Field";
import { Spinner } from "@/components/ui/States";
import { ApiError, api } from "@/services/apiClient";
import { useAuth } from "@/providers/AuthProvider";
import { useI18n } from "@/providers/I18nProvider";
import { postLoginRoute } from "@/features/onboarding/steps";
import type { DemoPatient, OtpRequestResult, Session } from "@/types/api";

type Stage = "mobile" | "code";

export function LoginPage() {
  const { t, s, language } = useI18n();
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const [stage, setStage] = useState<Stage>("mobile");
  const [mobile, setMobile] = useState("");
  const [code, setCode] = useState("");
  const [challenge, setChallenge] = useState<OtpRequestResult | null>(null);
  const [showDemoPersonas, setShowDemoPersonas] = useState(false);

  const demoPatients = useQuery({
    queryKey: ["demo-patients"],
    queryFn: () => api.get<DemoPatient[]>("/auth/demo-patients"),
    staleTime: Infinity,
  });

  const requestCode = useMutation({
    mutationFn: (value: string) =>
      api.post<OtpRequestResult>("/auth/otp/request", {
        mobile_number: value,
        language,
      }),
    onSuccess: (result) => {
      setChallenge(result);
      setStage("code");
      // There is no SMS gateway, so the server hands the code back. Filling
      // the field is the honest presentation: the patient can see it, change
      // it, and continue — without a banner announcing the mechanism.
      setCode(result.prototype_code ?? "");
    },
  });

  const verify = useMutation({
    mutationFn: () =>
      api.post<Session>("/auth/otp/verify", {
        mobile_number: challenge?.mobile_number ?? mobile,
        code,
        language,
      }),
    onSuccess: (session) => {
      signIn(session);
      navigate(
        postLoginRoute(session.onboarding.next_route, session.onboarding.is_complete),
        { replace: true },
      );
    },
  });

  const demoLogin = useMutation({
    mutationFn: (demoKey: string) =>
      api.post<Session>("/auth/demo-login", { demo_key: demoKey }),
    onSuccess: (session) => {
      signIn(session);
      navigate(
        postLoginRoute(session.onboarding.next_route, session.onboarding.is_complete),
        { replace: true },
      );
    },
  });

  const errorOf = (error: unknown): string | null =>
    error instanceof ApiError ? error.message : error ? t("errorGeneric") : null;

  return (
    <AppShell wide showNav={false}>
      <div className="mx-auto max-w-5xl py-2 sm:py-6">
        {/* Clear, accessible back navigation to Home */}
        <div className="mb-6">
          <Link
            to="/"
            className="group inline-flex items-center gap-2 rounded-lg px-2 py-1 text-sm font-semibold text-ink-muted transition-colors hover:text-primary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
          >
            <ArrowLeft className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" aria-hidden="true" />
            <span>{t("backToHome")}</span>
          </Link>
        </div>

        <div className="grid gap-8 lg:grid-cols-12 lg:items-start">
          {/* Left Column: Brand Story & Trust Foundation */}
          <div className="space-y-6 lg:col-span-5 lg:pr-4">
            <div className="space-y-3">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/25 bg-primary-soft px-3 py-1 text-xs font-semibold text-primary-ink">
                <ShieldCheck className="h-4 w-4 text-primary" aria-hidden="true" />
                {t("loginSecureBadge")}
              </span>
              <h1 className="text-3xl font-bold leading-tight text-ink sm:text-4xl">
                {t("loginHeroHeading")}
              </h1>
              <p className="text-base text-ink-muted sm:text-lg">
                {t("loginHeroSubhead")}
              </p>
            </div>

            {/* Feature Highlights */}
            <div className="space-y-4 pt-2">
              <div className="flex items-start gap-3 rounded-xl border border-line bg-surface p-3.5 shadow-sm">
                <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary">
                  <Sparkles className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h2 className="text-sm font-semibold text-ink">{t("loginFeature1Title")}</h2>
                  <p className="mt-0.5 text-xs text-ink-muted">{t("loginFeature1Body")}</p>
                </div>
              </div>

              <div className="flex items-start gap-3 rounded-xl border border-line bg-surface p-3.5 shadow-sm">
                <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary">
                  <Volume2 className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h2 className="text-sm font-semibold text-ink">{t("loginFeature2Title")}</h2>
                  <p className="mt-0.5 text-xs text-ink-muted">{t("loginFeature2Body")}</p>
                </div>
              </div>

              <div className="flex items-start gap-3 rounded-xl border border-line bg-surface p-3.5 shadow-sm">
                <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary">
                  <CheckCircle2 className="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h2 className="text-sm font-semibold text-ink">{t("loginFeature3Title")}</h2>
                  <p className="mt-0.5 text-xs text-ink-muted">{t("loginFeature3Body")}</p>
                </div>
              </div>
            </div>

          </div>

          {/* Right Column: Authentication Card & Sample Personas */}
          <div className="space-y-6 lg:col-span-7">
            <Card className="border-line shadow-md">
              <div className="border-b border-line px-6 py-5">
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white shadow-sm">
                    {stage === "mobile" ? (
                      <Phone className="h-5 w-5" aria-hidden="true" />
                    ) : (
                      <KeyRound className="h-5 w-5" aria-hidden="true" />
                    )}
                  </span>
                  <div>
                    <h2 className="text-xl font-bold text-ink">{t("loginHeading")}</h2>
                    <p className="text-sm text-ink-muted">
                      {stage === "mobile" ? t("loginBody") : t("codeHint")}
                    </p>
                  </div>
                </div>
              </div>

              <CardBody className="p-6">
                {stage === "mobile" ? (
                  <form
                    className="space-y-5"
                    onSubmit={(event) => {
                      event.preventDefault();
                      requestCode.mutate(mobile);
                    }}
                  >
                    <Field
                      label={t("mobileLabel")}
                      hint={t("mobileHint")}
                      required
                      error={errorOf(requestCode.error)}
                    >
                      {({ inputId, describedBy, invalid }) => (
                        <div className="relative flex items-center">
                          <span className="absolute left-3.5 flex items-center gap-1.5 font-medium text-ink-muted select-none text-base border-r border-line pr-2.5">
                            <span className="text-xs font-semibold text-primary">IN</span> +91
                          </span>
                          <Input
                            id={inputId}
                            aria-describedby={describedBy}
                            aria-invalid={invalid}
                            type="tel"
                            inputMode="numeric"
                            autoComplete="tel"
                            autoFocus
                            value={mobile}
                            onChange={(event) => setMobile(event.target.value)}
                            placeholder="98765 43210"
                            className="pl-24 text-lg font-medium tracking-wide"
                          />
                        </div>
                      )}
                    </Field>

                    <Button
                      type="submit"
                      size="xl"
                      block
                      disabled={mobile.trim().length < 10 || requestCode.isPending}
                      className="shadow-sm"
                    >
                      {requestCode.isPending ? (
                        <Spinner label={t("sendingCode")} className="text-white" />
                      ) : (
                        <>
                          <span>{t("sendCode")}</span>
                          <ArrowRight className="h-5 w-5" aria-hidden="true" />
                        </>
                      )}
                    </Button>
                  </form>
                ) : (
                  <form
                    className="space-y-5"
                    onSubmit={(event) => {
                      event.preventDefault();
                      verify.mutate();
                    }}
                  >
                    <div className="rounded-xl border border-line bg-surface-muted p-4">
                      <p className="text-sm text-ink-muted">{t("codeSentTo")}</p>
                      <p className="mt-0.5 text-lg font-bold text-ink">
                        +91 {challenge?.mobile_number ?? mobile}
                      </p>
                    </div>

                    <Field
                      label={t("codeLabel")}
                      hint={challenge?.is_prototype_delivery ? t("codeNoSms") : undefined}
                      required
                      error={errorOf(verify.error)}
                    >
                      {({ inputId, describedBy, invalid }) => (
                        <Input
                          id={inputId}
                          aria-describedby={describedBy}
                          aria-invalid={invalid}
                          type="text"
                          inputMode="numeric"
                          autoComplete="one-time-code"
                          autoFocus
                          maxLength={6}
                          value={code}
                          onChange={(event) => setCode(event.target.value.replace(/\D/g, ""))}
                          className="text-center font-mono text-2xl tracking-[0.4em]"
                        />
                      )}
                    </Field>

                    <Button
                      type="submit"
                      size="xl"
                      block
                      disabled={code.length < 4 || verify.isPending}
                      className="shadow-sm"
                    >
                      {verify.isPending ? (
                        <Spinner label={t("verifying")} className="text-white" />
                      ) : (
                        t("verifyAndContinue")
                      )}
                    </Button>

                    <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-line">
                      <Button
                        variant="ghost"
                        size="md"
                        onClick={() => requestCode.mutate(challenge?.mobile_number ?? mobile)}
                        disabled={requestCode.isPending}
                      >
                        {t("resendCode")}
                      </Button>
                      <Button
                        variant="ghost"
                        size="md"
                        onClick={() => {
                          setStage("mobile");
                          setChallenge(null);
                          verify.reset();
                        }}
                      >
                        {t("changeNumber")}
                      </Button>
                    </div>
                  </form>
                )}
              </CardBody>
            </Card>

            {/* Sample Personas: Professional, clearly-labeled testing profiles */}
            <div className="rounded-2xl border border-line bg-surface p-5 shadow-sm">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="flex min-w-0 items-start gap-3">
                  <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary">
                    <TestTube2 className="h-5 w-5" aria-hidden="true" />
                  </span>
                  <div className="min-w-0">
                    <h3 className="text-base font-bold text-ink">{t("demoHeading")}</h3>
                    <p className="mt-0.5 text-xs text-ink-muted">
                      {t("demoBody")}
                    </p>
                  </div>
                </div>

                <Button
                  variant="ghost"
                  size="md"
                  onClick={() => setShowDemoPersonas((prev) => !prev)}
                  aria-expanded={showDemoPersonas}
                  aria-controls="demo-patient-list"
                  className="shrink-0 text-xs font-semibold"
                >
                  {showDemoPersonas ? (
                    <>
                      <span>{t("demoHide")}</span>
                      <ChevronUp className="ml-1 h-4 w-4" aria-hidden="true" />
                    </>
                  ) : (
                    <>
                      <span>
                        {t("demoShow")}
                        {demoPatients.data ? ` (${demoPatients.data.length})` : ""}
                      </span>
                      <ChevronDown className="ml-1 h-4 w-4" aria-hidden="true" />
                    </>
                  )}
                </Button>
              </div>

              {demoLogin.error && (
                <div className="mt-3">
                  <Alert tone="warning">{errorOf(demoLogin.error) ?? t("demoUnavailable")}</Alert>
                </div>
              )}

              {demoPatients.isLoading && (
                <div className="mt-3 py-2 text-center">
                  <Spinner label={t("loading")} />
                </div>
              )}

              {/* Collapsed by default so the sign-in form stays the primary
                  action; `hidden` keeps it out of the accessibility tree too,
                  which is what the toggle's aria-expanded promises. */}
              <div id="demo-patient-list" className="mt-4 space-y-2.5" hidden={!showDemoPersonas}>
                {demoPatients.data?.map((patient) => (
                  <button
                    key={patient.demo_key}
                    type="button"
                    onClick={() => {
                      // `isPending` has not flushed yet on a second synchronous
                      // tap, so check the mutation itself before firing again.
                      if (demoLogin.isPending) return;
                      demoLogin.mutate(patient.demo_key);
                    }}
                    disabled={demoLogin.isPending}
                    className="flex w-full min-h-touch items-center justify-between gap-3 rounded-xl border border-line bg-surface-muted px-4 py-3 text-left transition-all hover:border-primary hover:bg-primary-soft/50 hover:shadow-sm disabled:opacity-60 group"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary font-bold text-sm">
                        {s(patient.label).charAt(0)}
                      </span>
                      <div className="min-w-0">
                        <p className="truncate font-semibold text-ink group-hover:text-primary">
                          {s(patient.label)}
                        </p>
                        <p className="truncate text-xs text-ink-muted">
                          {s(patient.description)}
                        </p>
                      </div>
                    </div>
                    <span className="shrink-0 flex items-center gap-1 text-xs font-bold text-primary group-hover:underline">
                      <span>{t("continue")}</span>
                      <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
                    </span>
                  </button>
                ))}

                {demoPatients.data?.length === 0 && (
                  <Alert tone="warning">{t("demoUnavailable")}</Alert>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}

