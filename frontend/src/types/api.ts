/**
 * The API contract, mirrored from the backend Pydantic schemas.
 *
 * These unions intentionally use the same string values as the Python enums
 * in `app/shared/enums.py`. Keeping them literal (rather than `string`) means
 * a backend rename shows up as a TypeScript error rather than a runtime bug.
 */

export type Language = "en" | "hi" | "mr" | "ta" | "gu" | "pa";

/**
 * A localised value from the API. Only translated languages are present, so
 * a consumer must resolve it through the fallback chain rather than indexing.
 */
export type Localised = Partial<Record<Language, string>> & { en: string };
export type Gender = "male" | "female" | "other" | "undisclosed";

export type OnboardingStatus =
  | "abha_pending"
  | "personal_info_pending"
  | "assessment_pending"
  | "preferences_pending"
  | "consent_pending"
  | "medical_profile_pending"
  | "completed";

export type AbhaVerificationStatus = "unverified" | "verified" | "failed" | "skipped";

export type InterfaceMode = "standard" | "easy";
export type FontSize = "normal" | "large" | "extra_large";
export type ContrastMode = "normal" | "high";
export type InteractionPreference = "voice" | "touch" | "hybrid";
export type PreferenceSource = "recommended" | "customized";

export type DigitalComfort =
  | "very_comfortable"
  | "somewhat_comfortable"
  | "need_help"
  | "prefer_simple";
export type PreferredInteraction = "speaking" | "touching" | "both";
export type DifficultyLevel = "none" | "sometimes" | "yes";
export type AccessibilityNeed =
  | "low_literacy"
  | "low_vision"
  | "hard_of_hearing"
  | "limited_hand_mobility"
  | "needs_assistant"
  | "prefers_sign_language";

export type ConsentPurpose =
  | "health_data_collection"
  | "share_with_treating_doctor"
  | "abha_linkage";
export type ConsentStatus = "granted" | "declined" | "revoked";

export type DocumentType = "prescription" | "lab_report" | "discharge_summary" | "other";
export type ProcessingStatus =
  | "pending"
  | "processing"
  | "completed"
  | "failed"
  | "needs_review";

// --- Patient ---------------------------------------------------------------

export interface OnboardingProgress {
  status: OnboardingStatus;
  step_number: number;
  total_steps: number;
  percent: number;
  next_route: string;
  is_complete: boolean;
}

export interface Patient {
  id: string;
  full_name: string | null;
  display_name: string;
  mobile_number: string;
  date_of_birth: string | null;
  /** Derived server-side from date_of_birth. */
  age: number | null;
  gender: Gender | null;
  preferred_language: Language;
  emergency_contact_name: string | null;
  emergency_contact_number: string | null;
  emergency_contact_relation: string | null;
  onboarding_status: OnboardingStatus;
  /** Pre-selected next visit so a returning patient is not asked cold. */
  preferred_care_system: CareSystem | null;
  is_demo: boolean;
  created_at: string;
}

export interface PersonalInfoPayload {
  full_name?: string | null;
  date_of_birth?: string | null;
  gender?: Gender | null;
  preferred_language?: Language | null;
  emergency_contact_name?: string | null;
  emergency_contact_number?: string | null;
  emergency_contact_relation?: string | null;
}

// --- Auth ------------------------------------------------------------------

export interface OtpRequestResult {
  mobile_number: string;
  expires_at: string;
  expires_in_seconds: number;
  is_prototype_delivery: boolean;
  prototype_code: string | null;
}

export interface Session {
  access_token: string;
  token_type: string;
  expires_in_seconds: number;
  patient: Patient;
  onboarding: OnboardingProgress;
  is_new_patient: boolean;
}

export interface DemoPatient {
  demo_key: string;
  label: Localised;
  description: Localised;
  mobile_number: string;
}

// --- ABHA ------------------------------------------------------------------

export interface AbhaProfile {
  abha_id: string | null;
  verification_status: AbhaVerificationStatus;
  linked_at: string | null;
  failure_reason: string | null;
  is_mock: boolean;
}

export interface AbhaStepResult {
  abha: AbhaProfile;
  onboarding_status: OnboardingStatus;
  next_route: string;
  notice: string | null;
}

// --- Accessibility ---------------------------------------------------------

export interface AssessmentOption {
  value: string;
  label: Localised;
  help?: Localised;
  icon?: string;
}

export interface AssessmentQuestion {
  id: string;
  field: string;
  kind: "single" | "multiple";
  required: boolean;
  prompt: Localised;
  help: Localised;
  options: AssessmentOption[];
}

export interface AssessmentContent {
  questions: AssessmentQuestion[];
  preference_options: Record<string, AssessmentOption[]>;
}

export interface AssessmentPayload {
  digital_comfort: DigitalComfort;
  preferred_interaction: PreferredInteraction;
  reading_difficulty: DifficultyLevel;
  hearing_difficulty: DifficultyLevel;
  vision_difficulty: DifficultyLevel;
  additional_needs: AccessibilityNeed[];
  additional_notes?: string | null;
}

export interface RecommendationReason {
  code: string;
  en: string;
  hi: string;
}

export interface Recommendation {
  interface_mode: InterfaceMode;
  font_size: FontSize;
  contrast_mode: ContrastMode;
  audio_guidance: boolean;
  interaction_preference: InteractionPreference;
  language: Language;
  easy_mode_score: number;
  easy_mode_threshold: number;
  reasons: RecommendationReason[];
}

export interface Preferences {
  interface_mode: InterfaceMode;
  font_size: FontSize;
  contrast_mode: ContrastMode;
  audio_guidance: boolean;
  interaction_preference: InteractionPreference;
  language: Language;
  source: PreferenceSource;
  updated_at: string | null;
}

export interface PreferencesPayload {
  interface_mode?: InterfaceMode;
  font_size?: FontSize;
  contrast_mode?: ContrastMode;
  audio_guidance?: boolean;
  interaction_preference?: InteractionPreference;
  language?: Language;
  accepted_recommendation: boolean;
}

export interface AssessmentResult {
  assessment_id: string;
  recommendation: Recommendation;
  preferences: Preferences;
  onboarding_status: OnboardingStatus;
  next_route: string;
}

// --- Consent ---------------------------------------------------------------

export interface ConsentItemContent {
  purpose: ConsentPurpose;
  required: boolean;
  title: Localised;
  what: Localised;
  why: Localised;
  how: Localised;
}

export interface ConsentContent {
  version: string;
  summary: { title: Localised; body: Localised; withdraw: Localised };
  items: ConsentItemContent[];
}

export interface Consent {
  purpose: ConsentPurpose;
  status: ConsentStatus;
  text_version: string;
  language: string;
  granted_at: string | null;
  declined_at: string | null;
  revoked_at: string | null;
  is_active: boolean;
}

export interface ConsentState {
  consents: Consent[];
  has_required_consents: boolean;
  onboarding_status: OnboardingStatus;
  next_route: string;
}

// --- Medical profile -------------------------------------------------------

export interface ClinicalItem {
  value: string;
  attributes: Record<string, string>;
  source: "patient" | "document" | "previous_record" | "clinician";
  confidence: number;
  verified: boolean;
  document_id: string | null;
  note: string | null;
  recorded_at: string;
}

export interface MedicalSectionContent {
  key: string;
  title: Localised;
  prompt: Localised;
  placeholder: Localised;
  icon: string;
  important?: boolean;
  suggestions: Localised[];
}

export interface MedicalProfile {
  sections: Record<string, ClinicalItem[]>;
  total_items: number;
  updated_at: string | null;
  onboarding_status: OnboardingStatus;
  next_route: string;
}

export interface MedicalItemPayload {
  value: string;
  attributes?: Record<string, string>;
  note?: string | null;
}

// --- Documents -------------------------------------------------------------

/**
 * Who issued a document, read from its printed letterhead.
 *
 * Every field is optional and absent when it could not be read — a missing
 * key means "not found", never blank. A wrong clinician name presented as
 * fact would be worse than showing nothing.
 */
export interface DocumentLetterhead {
  facility?: string;
  clinician?: string;
  qualifications?: string;
  department?: string;
  patient_name?: string;
  phone?: string;
}

export interface MedicalDocument {
  id: string;
  document_type: DocumentType;
  title: string | null;
  file_name: string;
  mime_type: string;
  size_bytes: number;
  processing_status: ProcessingStatus;
  processing_error: string | null;
  /** Raw OCR text, kept even when extraction found nothing (Phase 2). */
  ocr_text?: string | null;
  ocr_engine?: string | null;
  ocr_confidence?: number | null;
  /** Date printed on the document, used to place it on the timeline. */
  document_date?: string | null;
  extracted_items?: ExtractedItem[];
  extracted_data?: { letterhead?: DocumentLetterhead } & Record<string, unknown> | null;
  created_at: string;
}

export interface DocumentList {
  documents: MedicalDocument[];
  total: number;
  onboarding_status: OnboardingStatus;
  next_route: string;
}

// --- Aggregated profile ----------------------------------------------------

export interface PatientProfile {
  patient: Patient;
  onboarding: OnboardingProgress;
  abha: AbhaProfile | null;
  preferences: Preferences | null;
  consents: Array<{
    purpose: ConsentPurpose;
    status: ConsentStatus;
    granted_at: string | null;
    revoked_at: string | null;
  }>;
  medical_profile: { sections: Record<string, number>; total_items: number };
  document_count: number;
  encounter_count: number;
  last_assessment_at: string | null;
}

// ===========================================================================
// Phase 2
// ===========================================================================

export type InputMethod = "voice" | "text" | "touch";
export type ConversationStatus =
  | "in_progress"
  | "awaiting_review"
  | "confirmed"
  | "abandoned";
export type AnswerKind =
  | "single_choice"
  | "multi_choice"
  | "free_text"
  | "list"
  | "yes_no"
  | "scale"
  | "number";

export type ExtractedEntityType =
  | "diagnosis"
  | "medication"
  | "investigation"
  | "procedure"
  | "surgery"
  | "allergy"
  | "vital"
  | "note";
export type LabFlag = "normal" | "low" | "high" | "unclear";
export type ReviewState = "unreviewed" | "accepted" | "rejected";
export type TimelineEventType =
  | "document"
  | "diagnosis"
  | "medication"
  | "investigation"
  | "surgery"
  | "visit";

// --- Interview -------------------------------------------------------------

export interface InterviewQuestionOption {
  value: string;
  label: string;
  icon: string | null;
}

export interface InterviewQuestion {
  id: string;
  /** Identifies this exact asking, so a stale screen cannot answer it. */
  instance_key: string;
  section: string;
  section_title: string;
  section_intro: string;
  kind: AnswerKind;
  text: string;
  help: string;
  options: InterviewQuestionOption[];
  suggestions: string[];
  allow_none: boolean;
  required: boolean;
  is_ai_suggested: boolean;
  /** Non-empty for a per-item follow-up, e.g. "Diabetes". */
  about: string;
}

export interface InterviewProgress {
  answered: number;
  total: number;
  percent: number;
  section: string;
  section_index: number;
  section_count: number;
}

export interface InterviewView {
  session_id: string;
  status: ConversationStatus;
  question: InterviewQuestion | null;
  progress: InterviewProgress;
  complete: boolean;
  retry_hint: string | null;
  ai_fallback_active: boolean;
  language: Language;
}

export interface AnswerPayload {
  instance_key: string;
  text: string;
  input_method: InputMethod;
}

export interface AiStatus {
  provider: string;
  available: boolean;
  detail: string | null;
}

// --- Documents -------------------------------------------------------------

export interface ExtractedItem {
  id: string;
  entity_type: ExtractedEntityType;
  value: string;
  attributes: Record<string, string>;
  numeric_value: string | null;
  unit: string | null;
  reference_range: string | null;
  /** Only present when a reference range was printed on the document. */
  flag: LabFlag | null;
  event_date: string | null;
  confidence: number;
  review_state: ReviewState;
  extractor: string;
}

export interface DocumentStatus {
  id: string;
  processing_status: ProcessingStatus;
  processing_error: string | null;
  finding_count: number;
  message: Localised;
}

// --- Timeline --------------------------------------------------------------

export interface TimelineEvent {
  id: string;
  event_type: TimelineEventType;
  event_date: string | null;
  title: string;
  /** Free text quoted from a document, e.g. a dose. Already in its own language. */
  detail: string;
  /** An enum the client labels itself, when the detail is a status or a kind. */
  detail_kind: string;
  /** Where this came from — never presented as a confirmed fact. */
  source_kind: string;
  source_name: string;
  document_id: string | null;
  flag: LabFlag | null;
  requires_review: boolean;
}

export interface Timeline {
  events: TimelineEvent[];
  total: number;
  counts: Partial<Record<TimelineEventType, number>>;
  disclaimer: Localised;
}

// --- AYUSH -----------------------------------------------------------------

export interface AyushOption {
  value: string;
  label: Localised;
}

export interface AyushFactor {
  key: string;
  /** The Sanskrit term, transliterated in English and in Devanagari. */
  term: Localised;
  prompt: Localised;
  help: Localised;
  options: AyushOption[];
}

export interface AyushContent {
  intro: { title: Localised; body: Localised };
  dashavidha: AyushFactor[];
  /** Ashtasthana Pariksha — a practitioner confirms each at the couch. */
  ashtasthana: AyushFactor[];
  /** Agni/Koshtha, Nidra, Manas. */
  lifestyle: AyushFactor[];
  ahara_options: AyushOption[];
  vihara_options: AyushOption[];
  total_factors: number;
}

export interface AyushAssessment {
  dashavidha: Record<string, string>;
  ashtasthana: Record<string, string>;
  lifestyle: Record<string, string>;
  ahara: string[];
  vihara: string[];
  notes: string | null;
  is_complete: boolean;
  answered_count: number;
}

// --- Structured history ----------------------------------------------------

export interface HistoryEntry {
  value: string;
  attributes: Record<string, string>;
  source: "patient" | "document" | "previous_record" | "clinician";
  confidence: number;
  verified: boolean;
  /** A machine note kind, e.g. `found_in_document`, worded by the client. */
  note: string | null;
  /** The document a `found_in_document` note refers to. */
  note_source: string;
  document_id: string | null;
  flag?: LabFlag | null;
}

export interface StructuredHistory {
  sections: Record<string, HistoryEntry[]>;
  labels: Record<string, string>;
  patient_reported_count: number;
  document_derived_count: number;
  missing_sections: string[];
  ayush_included: boolean;
  narrative: string;
  narrative_source: "template" | "ai";
  disclaimer: Localised;
}

// ===========================================================================
// Phase 3
// ===========================================================================

export type RedFlagStatus = "none" | "active" | "clinician_cleared";
export type RedFlagCategory =
  | "breathing"
  | "chest"
  | "bleeding"
  | "consciousness"
  | "neurological"
  | "other";
export type RedFlagSource = "rules" | "ai_assist";
export type EncounterStatus =
  | "draft"
  | "in_progress"
  | "awaiting_review"
  | "completed"
  | "cancelled";
export type EncounterPriority = "routine" | "priority" | "urgent";
export type VisitType = "first_visit" | "follow_up";

/** Which system of medicine a visit is for — decides the interview length. */
export type CareSystem =
  | "allopathy"
  | "ayurveda"
  | "homoeopathy"
  | "unani"
  | "siddha"
  | "yoga_naturopathy"
  | "unsure";

export interface RedFlag {
  category: RedFlagCategory;
  source: RedFlagSource;
  /** The patient's own words. Never the criterion that matched. */
  evidence: string;
  created_at: string;
}

export interface SafetyNotice {
  title: Localised;
  body: Localised;
  disclaimer: Localised;
  action_staff: Localised;
  action_continue: Localised;
  instruction: Localised;
}

export interface RedFlagState {
  status: RedFlagStatus;
  flags: RedFlag[];
  notice: SafetyNotice | null;
  acknowledged: boolean;
  /** Always false — priority is not the patient's to change. */
  can_be_cleared_by_patient: boolean;
}

export interface ExistingContext {
  conditions: string[];
  medications: string[];
  allergies: string[];
  recent_documents: Array<{
    id: string;
    title: string;
    type: string;
    date: string | null;
    status: ProcessingStatus;
  }>;
  last_visit_at: string | null;
  last_visit_complaint: string | null;
}

export interface EncounterView {
  encounter_id: string;
  session_id: string | null;
  status: EncounterStatus;
  priority: EncounterPriority;
  visit_type: VisitType;
  care_system: CareSystem | null;
  chief_complaint: string | null;
  question: InterviewQuestion | null;
  progress: InterviewProgress;
  complete: boolean;
  retry_hint: string | null;
  ai_fallback_active: boolean;
  safety: RedFlagState;
  existing: ExistingContext;
  submitted_at: string | null;
  language: Language;
}

export interface TodayAnswer {
  question_text: string;
  answer: string;
  section: string;
  input_method: InputMethod;
}

/** One factor the patient answered in the Ayurvedic examination. */
export interface AyushReviewEntry {
  group: string;
  /** The Sanskrit term, or "" for a multi-select choice. */
  term: string;
  question: string;
  answer: string;
}

export interface AyushReview {
  count: number;
  total: number;
  entries: AyushReviewEntry[];
}

export interface EncounterReview {
  encounter_id: string;
  chief_complaint: string | null;
  today: Record<string, Array<{ value: string; source: string; confidence: number }>>;
  today_answers: TodayAnswer[];
  /** Questions the patient skipped — counted, not listed. */
  skipped_count: number;
  /** The 1-10 rating, rendered as a metric rather than an answer row. */
  severity: string | null;
  existing: ExistingContext;
  documents_today: Array<{ id: string; title: string; type: string; status: string }>;
  safety: RedFlagState;
  priority: EncounterPriority;
  narrative: string;
  narrative_source: "template" | "ai";
  labels: Record<string, string>;
  /** Present only when this visit ran an AYUSH examination. */
  ayush: AyushReview | null;
  missing: string[];
  disclaimer: Localised;
  submitted_at: string | null;
  patient_confirmed: boolean;
}

export interface EncounterSubmission {
  encounter_id: string;
  status: EncounterStatus;
  priority: EncounterPriority;
  submitted_at: string | null;
  message: Localised;
}

export interface PatientHome {
  patient: Patient;
  greeting: Localised;
  onboarding: OnboardingProgress;
  profile_complete: boolean;
  history_item_count: number;
  conditions: string[];
  medications: string[];
  allergies: string[];
  recent_documents: Array<{
    id: string;
    title: string;
    type: string;
    status: ProcessingStatus;
    date: string | null;
  }>;
  document_count: number;
  recent_events: TimelineEvent[];
  last_visit: {
    id: string;
    complaint: string | null;
    submitted_at: string;
    priority: EncounterPriority;
    was_urgent: boolean;
  } | null;
  visit_count: number;
  visit_in_progress: {
    id: string;
    complaint: string | null;
    started_at: string | null;
    is_urgent: boolean;
  } | null;
}
