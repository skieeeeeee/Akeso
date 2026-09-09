import { Suspense, lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { LandingPage } from "@/pages/LandingPage";
import { WelcomePage } from "@/pages/WelcomePage";
import { LoginPage } from "@/pages/LoginPage";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { LoadingPanel } from "@/components/ui/States";
import { RequireAuth, RequireStep } from "./guards";

// Split by route. The landing, language and sign-in screens stay in the
// main bundle because they are what a first-time visitor loads; every
// screen past sign-in is fetched when it is first opened. This matters
// more here than in most products: the app is aimed at patients on
// mid-range phones over mobile data, where one 600 KB bundle is a wait
// before anything is usable at all.
const AbhaPage = lazy(() => import("@/pages/AbhaPage").then((m) => ({ default: m.AbhaPage })));
const AssessmentPage = lazy(() => import("@/pages/AssessmentPage").then((m) => ({ default: m.AssessmentPage })));
const AyushPage = lazy(() => import("@/pages/AyushPage").then((m) => ({ default: m.AyushPage })));
const CompletePage = lazy(() => import("@/pages/CompletePage").then((m) => ({ default: m.CompletePage })));
const ConsentPage = lazy(() => import("@/pages/ConsentPage").then((m) => ({ default: m.ConsentPage })));
const HomePage = lazy(() => import("@/pages/HomePage").then((m) => ({ default: m.HomePage })));
const InterviewPage = lazy(() => import("@/pages/InterviewPage").then((m) => ({ default: m.InterviewPage })));
const MedicalProfilePage = lazy(() => import("@/pages/MedicalProfilePage").then((m) => ({ default: m.MedicalProfilePage })));
const PersonalInfoPage = lazy(() => import("@/pages/PersonalInfoPage").then((m) => ({ default: m.PersonalInfoPage })));
const PreferencesPage = lazy(() => import("@/pages/PreferencesPage").then((m) => ({ default: m.PreferencesPage })));
const ProfilePage = lazy(() => import("@/pages/ProfilePage").then((m) => ({ default: m.ProfilePage })));
const RecordsPage = lazy(() => import("@/pages/RecordsPage").then((m) => ({ default: m.RecordsPage })));
const ReviewPage = lazy(() => import("@/pages/ReviewPage").then((m) => ({ default: m.ReviewPage })));
const ScannedVisitPage = lazy(() => import("@/pages/ScannedVisitPage").then((m) => ({ default: m.ScannedVisitPage })));
const SettingsPage = lazy(() => import("@/pages/SettingsPage").then((m) => ({ default: m.SettingsPage })));
const TimelinePage = lazy(() => import("@/pages/TimelinePage").then((m) => ({ default: m.TimelinePage })));
const VisitPage = lazy(() => import("@/pages/VisitPage").then((m) => ({ default: m.VisitPage })));
const VisitReviewPage = lazy(() => import("@/pages/VisitReviewPage").then((m) => ({ default: m.VisitReviewPage })));

/** Every onboarding step is auth-guarded and progress-guarded. */
function Step({ children }: { children: React.ReactNode }) {
  return (
    <RequireAuth>
      <RequireStep>{children}</RequireStep>
    </RequireAuth>
  );
}

export function AppRoutes() {
  return (
    // One boundary for all of them: a route chunk is a single small
    // request, so a shared fallback avoids a spinner per page.
    <Suspense fallback={<LoadingPanel label="Loading…" />}>
      <Routes>
      {/* "/" is the public landing page; a kiosk is pinned to /start, which
          is the language-then-begin screen. */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/start" element={<WelcomePage />} />
      <Route path="/login" element={<LoginPage />} />

      <Route path="/onboarding/abha" element={<Step><AbhaPage /></Step>} />
      <Route path="/onboarding/personal" element={<Step><PersonalInfoPage /></Step>} />
      <Route path="/onboarding/assessment" element={<Step><AssessmentPage /></Step>} />
      <Route path="/onboarding/preferences" element={<Step><PreferencesPage /></Step>} />
      <Route path="/onboarding/consent" element={<Step><ConsentPage /></Step>} />
      <Route
        path="/onboarding/medical-profile"
        element={<Step><MedicalProfilePage /></Step>}
      />

      {/* Phase 2: the medical interview and everything downstream of it.
          These are auth-guarded but not part of the onboarding step sequence,
          so a patient can revisit any of them at any time. */}
      <Route path="/interview" element={<RequireAuth><InterviewPage /></RequireAuth>} />
      <Route path="/records" element={<RequireAuth><RecordsPage /></RequireAuth>} />
      <Route path="/timeline" element={<RequireAuth><TimelinePage /></RequireAuth>} />
      <Route path="/review" element={<RequireAuth><ReviewPage /></RequireAuth>} />
      <Route path="/ayush" element={<RequireAuth><AyushPage /></RequireAuth>} />

      {/* Records and completion sit after the guarded steps. */}
      <Route path="/onboarding/records" element={<RequireAuth><RecordsPage /></RequireAuth>} />
      <Route path="/onboarding/complete" element={<RequireAuth><CompletePage /></RequireAuth>} />
      <Route path="/profile" element={<RequireAuth><ProfilePage /></RequireAuth>} />

      {/* Phase 3: the returning-patient journey. */}
      <Route path="/home" element={<RequireAuth><HomePage /></RequireAuth>} />
      <Route path="/visit" element={<RequireAuth><VisitPage /></RequireAuth>} />
      <Route
        path="/visit/:encounterId/review"
        element={<RequireAuth><VisitReviewPage /></RequireAuth>}
      />
      <Route path="/settings" element={<RequireAuth><SettingsPage /></RequireAuth>} />

      {/* Legacy/short links people may type. */}
      {/* Scanned from the patient's QR code by a clinician who has no account
          here. Outside RequireAuth on purpose: the token in the URL is the
          authorisation, it names one visit, and it expires within the hour. */}
      <Route path="/handoff/:token" element={<ScannedVisitPage />} />

      <Route path="/onboarding" element={<Navigate to="/onboarding/abha" replace />} />
      <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}
