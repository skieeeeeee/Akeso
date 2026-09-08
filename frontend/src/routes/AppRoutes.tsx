import { Navigate, Route, Routes } from "react-router-dom";
import { LandingPage } from "@/pages/LandingPage";
import { WelcomePage } from "@/pages/WelcomePage";
import { LoginPage } from "@/pages/LoginPage";
import { AbhaPage } from "@/pages/AbhaPage";
import { PersonalInfoPage } from "@/pages/PersonalInfoPage";
import { ScannedVisitPage } from "@/pages/ScannedVisitPage";
import { AssessmentPage } from "@/pages/AssessmentPage";
import { PreferencesPage } from "@/pages/PreferencesPage";
import { ConsentPage } from "@/pages/ConsentPage";
import { MedicalProfilePage } from "@/pages/MedicalProfilePage";
import { RecordsPage } from "@/pages/RecordsPage";
import { CompletePage } from "@/pages/CompletePage";
import { ProfilePage } from "@/pages/ProfilePage";
import { InterviewPage } from "@/pages/InterviewPage";
import { TimelinePage } from "@/pages/TimelinePage";
import { ReviewPage } from "@/pages/ReviewPage";
import { AyushPage } from "@/pages/AyushPage";
import { HomePage } from "@/pages/HomePage";
import { VisitPage } from "@/pages/VisitPage";
import { VisitReviewPage } from "@/pages/VisitReviewPage";
import { SettingsPage } from "@/pages/SettingsPage";
import { NotFoundPage } from "@/pages/NotFoundPage";
import { RequireAuth, RequireStep } from "./guards";

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
  );
}
