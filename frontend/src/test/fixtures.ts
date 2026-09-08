import type { AssessmentContent, ConsentContent, Preferences } from "@/types/api";

export const PREFERENCES: Preferences = {
  interface_mode: "standard",
  font_size: "normal",
  contrast_mode: "normal",
  audio_guidance: false,
  interaction_preference: "touch",
  language: "en",
  source: "recommended",
  updated_at: null,
};

const t = (en: string, hi: string) => ({ en, hi });

export const ASSESSMENT_CONTENT: AssessmentContent = {
  questions: [
    {
      id: "digital_comfort",
      field: "digital_comfort",
      kind: "single",
      required: true,
      prompt: t("How comfortable are you using smartphones?", "स्मार्टफोन उपयोग में कितने सहज हैं?"),
      help: t("This changes how much we show.", "इससे तय होता है कि कितना दिखाएँ।"),
      options: [
        { value: "very_comfortable", label: t("Very comfortable", "बहुत सहज"), icon: "smartphone" },
        { value: "prefer_simple", label: t("I prefer a simpler experience", "आसान अनुभव पसंद है"), icon: "sparkles" },
      ],
    },
    {
      id: "preferred_interaction",
      field: "preferred_interaction",
      kind: "single",
      required: true,
      prompt: t("How would you prefer to answer?", "आप कैसे जवाब देना चाहेंगे?"),
      help: t("You can switch later.", "आप बाद में बदल सकते हैं।"),
      options: [
        { value: "touching", label: t("By touching options", "विकल्प छूकर"), icon: "hand" },
        { value: "speaking", label: t("By speaking", "बोलकर"), icon: "mic" },
      ],
    },
    {
      id: "reading_difficulty",
      field: "reading_difficulty",
      kind: "single",
      required: true,
      prompt: t("Difficulty reading screens?", "स्क्रीन पढ़ने में कठिनाई?"),
      help: t("We can enlarge text.", "हम टेक्स्ट बड़ा कर सकते हैं।"),
      options: [
        { value: "none", label: t("No difficulty", "कोई कठिनाई नहीं"), icon: "check" },
        { value: "yes", label: t("Yes", "हाँ"), icon: "alert" },
      ],
    },
    {
      id: "vision_difficulty",
      field: "vision_difficulty",
      kind: "single",
      required: true,
      prompt: t("Difficulty seeing screens?", "स्क्रीन देखने में कठिनाई?"),
      help: t("We can raise contrast.", "हम कंट्रास्ट बढ़ा सकते हैं।"),
      options: [
        { value: "none", label: t("No difficulty", "कोई कठिनाई नहीं"), icon: "check" },
        { value: "yes", label: t("Yes", "हाँ"), icon: "alert" },
      ],
    },
    {
      id: "hearing_difficulty",
      field: "hearing_difficulty",
      kind: "single",
      required: true,
      prompt: t("Difficulty hearing audio?", "आवाज़ सुनने में कठिनाई?"),
      help: t("Nothing will need sound.", "कुछ भी आवाज़ पर निर्भर नहीं होगा।"),
      options: [
        { value: "none", label: t("No difficulty", "कोई कठिनाई नहीं"), icon: "check" },
        { value: "yes", label: t("Yes", "हाँ"), icon: "alert" },
      ],
    },
    {
      id: "additional_needs",
      field: "additional_needs",
      kind: "multiple",
      required: false,
      prompt: t("Anything else that would help?", "कुछ और जो मदद करे?"),
      help: t("Completely optional.", "पूरी तरह वैकल्पिक।"),
      options: [
        { value: "low_literacy", label: t("Reading is difficult", "पढ़ना कठिन है"), icon: "book" },
      ],
    },
  ],
  preference_options: {
    interface_mode: [
      { value: "standard", label: t("Standard", "सामान्य"), help: t("All options on one screen", "सभी विकल्प एक स्क्रीन पर") },
      { value: "easy", label: t("Easy", "आसान"), help: t("One question at a time", "एक बार में एक सवाल") },
    ],
    font_size: [
      { value: "normal", label: t("Normal", "सामान्य") },
      { value: "large", label: t("Large", "बड़ा") },
      { value: "extra_large", label: t("Extra large", "अतिरिक्त बड़ा") },
    ],
    contrast_mode: [
      { value: "normal", label: t("Normal colours", "सामान्य रंग") },
      { value: "high", label: t("High contrast", "उच्च कंट्रास्ट") },
    ],
    interaction_preference: [
      { value: "touch", label: t("Touch", "छूकर") },
      { value: "voice", label: t("Voice", "बोलकर") },
      { value: "hybrid", label: t("Both", "दोनों") },
    ],
  },
};

export const CONSENT_CONTENT: ConsentContent = {
  version: "2026-01",
  summary: {
    title: t("Before we begin", "शुरू करने से पहले"),
    body: t("We will ask about your health.", "हम आपके स्वास्थ्य के बारे में पूछेंगे।"),
    withdraw: t("You can withdraw any time.", "आप कभी भी वापस ले सकते हैं।"),
  },
  items: [
    {
      purpose: "health_data_collection",
      required: true,
      title: t("Collecting your health information", "स्वास्थ्य जानकारी एकत्र करना"),
      what: t("Your symptoms and history.", "आपके लक्षण और इतिहास।"),
      why: t("So your doctor is prepared.", "जिससे डॉक्टर तैयार हों।"),
      how: t("Shown to your clinician.", "आपके चिकित्सक को दिखाया जाता है।"),
    },
    {
      purpose: "abha_linkage",
      required: false,
      title: t("Linking your health ID", "हेल्थ आईडी जोड़ना"),
      what: t("The health ID you entered.", "आपकी दर्ज हेल्थ आईडी।"),
      why: t("Records follow you.", "रिकॉर्ड आपके साथ चलते हैं।"),
      how: t("Prototype only.", "केवल प्रोटोटाइप।"),
    },
  ],
};

// --- Phase 2 ---------------------------------------------------------------

import type {
  InterviewQuestion,
  InterviewView,
  MedicalDocument,
  StructuredHistory,
  Timeline,
} from "@/types/api";

export function question(overrides: Partial<InterviewQuestion> = {}): InterviewQuestion {
  return {
    id: "q_chief_complaint",
    instance_key: "q_chief_complaint",
    section: "presenting",
    section_title: "Why you are here",
    section_intro: "First, tell us what brings you in today.",
    kind: "free_text",
    text: "What problem brings you in today?",
    help: "Describe it in your own words.",
    options: [],
    suggestions: ["Chest pain", "Fever"],
    allow_none: true,
    required: false,
    is_ai_suggested: false,
    about: "",
    ...overrides,
  };
}

export function interviewView(overrides: Partial<InterviewView> = {}): InterviewView {
  return {
    session_id: "sess-1",
    status: "in_progress",
    question: question(),
    progress: {
      answered: 0,
      total: 20,
      percent: 0,
      section: "presenting",
      section_index: 0,
      section_count: 9,
    },
    complete: false,
    retry_hint: null,
    ai_fallback_active: false,
    language: "en",
    ...overrides,
  };
}

export const AI_STATUS_OFF = { provider: "none", available: false, detail: null };

export function medicalDocument(overrides: Partial<MedicalDocument> = {}): MedicalDocument {
  return {
    id: "doc-1",
    document_type: "lab_report",
    title: "City Lab",
    file_name: "lab.txt",
    mime_type: "text/plain",
    size_bytes: 512,
    processing_status: "completed",
    processing_error: null,
    ocr_text: "Haemoglobin 10.2 g/dL (13.0-17.0)",
    ocr_engine: "plaintext",
    ocr_confidence: 1,
    document_date: "2026-03-10",
    extracted_items: [
      {
        id: "item-1",
        entity_type: "investigation",
        value: "Haemoglobin",
        attributes: {},
        numeric_value: "10.2",
        unit: "g/dL",
        reference_range: "13.0-17.0",
        flag: "low",
        event_date: "2026-03-10",
        confidence: 0.8,
        review_state: "unreviewed",
        extractor: "rules",
      },
    ],
    extracted_data: null,
    created_at: "2026-03-10T00:00:00Z",
    ...overrides,
  };
}

export const TIMELINE: Timeline = {
  events: [
    {
      id: "doc:doc-1",
      event_type: "document",
      event_date: "2026-03-10",
      title: "City Lab",
      detail: "lab report",
      detail_kind: "prescription",
      source_kind: "uploaded_document",
      source_name: "City Lab report",
      document_id: "doc-1",
      flag: null,
      requires_review: false,
    },
    {
      id: "item:item-1",
      event_type: "investigation",
      event_date: "2026-03-10",
      title: "Haemoglobin",
      detail: "10.2 g/dL (reference 13.0-17.0)",
      detail_kind: "",
      source_kind: "found_in_document",
      source_name: "City Lab",
      document_id: "doc-1",
      flag: "low",
      requires_review: true,
    },
  ],
  total: 2,
  counts: { document: 1, investigation: 1 },
  disclaimer: {
    en: "This is a record of what you told us. It is not a diagnosis.",
    hi: "यह निदान नहीं है।",
  },
};

export const STRUCTURED_HISTORY: StructuredHistory = {
  sections: {
    chief_complaint: [
      {
        value: "Chest pain",
        attributes: {},
        source: "patient",
        confidence: 1,
        verified: false,
        note: null,
        note_source: "",
        document_id: null,
      },
    ],
    current_medications: [
      {
        value: "Metformin",
        attributes: { dose: "500 mg", frequency: "BD" },
        source: "document",
        confidence: 0.75,
        verified: false,
        note: "found_in_document",
        note_source: "Dr Mehta",
        document_id: "doc-1",
      },
    ],
  },
  labels: {
    chief_complaint: "Chief complaint",
    current_medications: "Medications",
    allergies: "Allergies",
  },
  patient_reported_count: 1,
  document_derived_count: 1,
  missing_sections: ["allergies"],
  ayush_included: false,
  narrative: "Patient reports chest pain. This is not a diagnosis.",
  narrative_source: "template",
  disclaimer: {
    en: "This is not a diagnosis, and your doctor will go through it with you.",
    hi: "यह निदान नहीं है।",
  },
};

// --- Phase 3 ---------------------------------------------------------------

import type {
  EncounterReview,
  EncounterView,
  ExistingContext,
  PatientHome,
  RedFlagState,
} from "@/types/api";

export const EXISTING: ExistingContext = {
  conditions: ["Type 2 diabetes mellitus", "Hypertension"],
  medications: ["Metformin 500 mg", "Telmisartan 40 mg"],
  allergies: ["Sulfa drugs"],
  recent_documents: [
    { id: "doc-1", title: "City Lab", type: "lab_report", date: "2026-03-10", status: "completed" },
  ],
  last_visit_at: "2026-06-05T10:00:00Z",
  last_visit_complaint: "Routine diabetes review",
};

export const SAFETY_CLEAR: RedFlagState = {
  status: "none",
  flags: [],
  notice: null,
  acknowledged: false,
  can_be_cleared_by_patient: false,
};

export const SAFETY_ACTIVE: RedFlagState = {
  status: "active",
  flags: [
    {
      category: "chest",
      source: "rules",
      evidence: "I have crushing chest pain going into my left arm",
      created_at: "2026-09-07T10:00:00Z",
    },
  ],
  notice: {
    title: {
      en: "Please speak to healthcare staff now",
      hi: "कृपया अभी स्वास्थ्य कर्मचारियों से बात करें",
    },
    body: {
      en: "Some of the symptoms you described may require urgent medical attention.",
      hi: "आपने जो लक्षण बताए, उनके लिए तत्काल चिकित्सा सहायता की आवश्यकता हो सकती है।",
    },
    disclaimer: {
      en: "This does not confirm a medical condition.",
      hi: "यह किसी बीमारी की पुष्टि नहीं करता।",
    },
    action_staff: { en: "I need immediate assistance", hi: "मुझे तुरंत सहायता चाहिए" },
    action_continue: {
      en: "Continue answering while waiting",
      hi: "इंतज़ार करते हुए जवाब देना जारी रखें",
    },
    instruction: {
      en: "Please inform nearby healthcare staff immediately.",
      hi: "कृपया तुरंत पास के स्वास्थ्य कर्मचारियों को बताएं।",
    },
  },
  acknowledged: false,
  can_be_cleared_by_patient: false,
};

export function encounterView(overrides: Partial<EncounterView> = {}): EncounterView {
  return {
    encounter_id: "enc-1",
    session_id: "sess-2",
    status: "in_progress",
    priority: "routine",
    visit_type: "follow_up",
    care_system: "allopathy",
    chief_complaint: null,
    question: question({
      id: "e_complaint",
      instance_key: "e_complaint",
      section: "today",
      section_title: "Today's concern",
      text: "What brings you here today?",
      suggestions: ["Fever", "Cough", "Pain"],
    }),
    progress: {
      answered: 0,
      total: 11,
      percent: 0,
      section: "today",
      section_index: 0,
      section_count: 3,
    },
    complete: false,
    retry_hint: null,
    ai_fallback_active: false,
    safety: SAFETY_CLEAR,
    existing: EXISTING,
    submitted_at: null,
    language: "en",
    ...overrides,
  };
}

export const HOME: PatientHome = {
  patient: { ...PATIENT_FOR_HOME() },
  greeting: { en: "Welcome back", hi: "आपका फिर से स्वागत है" },
  onboarding: {
    status: "completed",
    step_number: 6,
    total_steps: 6,
    percent: 100,
    next_route: "/profile",
    is_complete: true,
  },
  profile_complete: true,
  history_item_count: 12,
  conditions: EXISTING.conditions,
  medications: EXISTING.medications,
  allergies: EXISTING.allergies,
  recent_documents: [
    {
      id: "doc-1",
      title: "City Lab",
      type: "lab_report",
      status: "completed",
      date: "2026-03-10",
    },
  ],
  document_count: 1,
  recent_events: TIMELINE.events,
  last_visit: {
    id: "enc-0",
    complaint: "Routine diabetes review",
    submitted_at: "2026-06-05T10:00:00Z",
    priority: "routine",
    was_urgent: false,
  },
  visit_count: 2,
  visit_in_progress: null,
};

function PATIENT_FOR_HOME() {
  return {
    id: "pat-1",
    full_name: "Rajesh Kumar",
    display_name: "Rajesh Kumar",
    mobile_number: "9812340001",
    date_of_birth: "1974-03-15",
    age: 52,
    gender: "male" as const,
    preferred_language: "en" as const,
    emergency_contact_name: null,
    emergency_contact_number: null,
    emergency_contact_relation: null,
    onboarding_status: "completed" as const,
    preferred_care_system: "allopathy" as const,
    is_demo: true,
    created_at: "2026-01-01T00:00:00Z",
  };
}

export const ENCOUNTER_REVIEW: EncounterReview = {
  // An allopathic visit: no AYUSH examination was run.
  ayush: null,
  encounter_id: "enc-1",
  chief_complaint: "Stomach pain since yesterday",
  today: {
    history_of_present_illness: [
      { value: "Cramping around the navel", source: "patient", confidence: 1 },
    ],
    current_medications: [{ value: "Pantoprazole 40 mg", source: "patient", confidence: 1 }],
  },
  today_answers: [
    {
      question_text: "What brings you here today?",
      answer: "Stomach pain since yesterday",
      section: "today",
      input_method: "voice",
    },
    {
      question_text: "When did it start?",
      answer: "Yesterday",
      section: "detail",
      input_method: "touch",
    },
  ],
  skipped_count: 3,
  severity: "5/10",
  existing: EXISTING,
  documents_today: [],
  safety: SAFETY_CLEAR,
  priority: "routine",
  narrative:
    "Rajesh Kumar (52-year-old, male) returns reporting stomach pain since yesterday. Not a diagnosis.",
  narrative_source: "template",
  labels: {
    history_of_present_illness: "History of present illness",
    current_medications: "Medications",
    chief_complaint: "Chief complaint",
  },
  missing: [],
  disclaimer: {
    en: "It is not a diagnosis, and a healthcare professional will review it with you.",
    hi: "यह निदान नहीं है।",
  },
  submitted_at: null,
  patient_confirmed: false,
};


export const AYUSH_CONTENT = {
  intro: {
    title: { en: "Ayurveda assessment", hi: "आयुर्वेद मूल्यांकन" },
    body: { en: "Optional questions used in Ayurvedic practice.", hi: "वैकल्पिक सवाल।" },
  },
  dashavidha: [
    {
      key: "prakriti",
      term: { en: "Prakriti", hi: "प्रकृति" },
      prompt: { en: "Which best describes your natural build?", hi: "आपकी बनावट?" },
      help: { en: "Your lifelong tendency.", hi: "आपकी प्रवृत्ति।" },
      options: [
        { value: "vata", label: { en: "Thin build", hi: "पतली बनावट" } },
        { value: "kapha", label: { en: "Heavier build", hi: "भारी बनावट" } },
      ],
    },
  ],
  ashtasthana: [
    {
      key: "nadi",
      term: { en: "Nadi", hi: "नाड़ी" },
      prompt: { en: "How does your pulse usually feel?", hi: "नाड़ी कैसी लगती है?" },
      help: { en: "A practitioner will check properly.", hi: "वैद्य ठीक से देखेंगे।" },
      options: [
        { value: "normal", label: { en: "Normal and steady", hi: "सामान्य" } },
        { value: "fast", label: { en: "Often fast", hi: "तेज़" } },
      ],
    },
  ],
  lifestyle: [
    {
      key: "manas",
      term: { en: "Manas", hi: "मनस्" },
      prompt: { en: "How has your mind felt lately?", hi: "मन कैसा रहा?" },
      help: { en: "Only if you wish to say.", hi: "यदि बताना चाहें।" },
      options: [
        { value: "calm", label: { en: "Calm and steady", hi: "शांत" } },
        { value: "prefer_not", label: { en: "I would rather not say", hi: "बताना नहीं चाहता" } },
      ],
    },
  ],
  ahara_options: [{ value: "vegetarian", label: { en: "Vegetarian", hi: "शाकाहारी" } }],
  vihara_options: [{ value: "early_riser", label: { en: "I wake up early", hi: "जल्दी उठता हूँ" } }],
  total_factors: 24,
};
