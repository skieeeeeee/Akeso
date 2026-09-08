/**
 * Human labels for the enum values the API sends.
 *
 * The API sends machine values (`needs_review`, `lab_report`) for anything
 * the client has to branch on; only free prose is localised server-side.
 * Without this map those values reach the screen as English-ish slugs, so a
 * Hindi patient sees "needs review" in the middle of a Hindi page.
 *
 * The map is flat, keyed by the raw value rather than by enum, because every
 * value that appears in more than one enum means the same thing in all of
 * them (`normal` font size / contrast / lab flag; `other` gender / document
 * type). If a future value ever needs two different labels depending on
 * context, give that call site its own map rather than bending this one.
 */
import { localised } from "@/services/apiClient";
import type { Language, LabFlag } from "@/types/api";
import { translate, withOverlay, type Translations } from "@/lib/strings";

export const ENUM_LABELS = {
  // --- Processing / verification lifecycle -------------------------------
  pending: { en: "Pending", hi: "प्रतीक्षा में" },
  processing: { en: "Processing", hi: "प्रक्रिया में" },
  completed: { en: "Completed", hi: "पूर्ण" },
  failed: { en: "Could not be read", hi: "पढ़ा नहीं जा सका" },
  needs_review: { en: "Needs your review", hi: "आपकी समीक्षा चाहिए" },
  unverified: { en: "Not verified", hi: "सत्यापित नहीं" },
  verified: { en: "Verified", hi: "सत्यापित" },
  skipped: { en: "Skipped", hi: "छोड़ा गया" },

  // --- Consent -----------------------------------------------------------
  granted: { en: "Given", hi: "दी गई" },
  declined: { en: "Declined", hi: "मना किया" },
  revoked: { en: "Withdrawn", hi: "वापस ली गई" },
  health_data_collection: {
    en: "Collecting your health information",
    hi: "आपकी स्वास्थ्य जानकारी एकत्र करना",
  },
  share_with_treating_doctor: {
    en: "Sharing with the doctor treating you",
    hi: "आपका इलाज करने वाले डॉक्टर के साथ साझा करना",
  },
  abha_linkage: { en: "Linking your ABHA number", hi: "आपका आभा नंबर जोड़ना" },

  // --- Documents ---------------------------------------------------------
  prescription: { en: "Prescription", hi: "पर्चा" },
  lab_report: { en: "Lab report", hi: "जाँच रिपोर्ट" },
  discharge_summary: { en: "Discharge summary", hi: "डिस्चार्ज सारांश" },
  other: { en: "Other", hi: "अन्य" },

  // --- Gender ------------------------------------------------------------
  male: { en: "Male", hi: "पुरुष" },
  female: { en: "Female", hi: "महिला" },
  undisclosed: { en: "Prefer not to say", hi: "बताना नहीं चाहते" },

  // --- Preferences -------------------------------------------------------
  standard: { en: "Standard", hi: "मानक" },
  easy: { en: "Easy Mode", hi: "आसान मोड" },
  normal: { en: "Normal", hi: "सामान्य" },
  large: { en: "Large", hi: "बड़ा" },
  extra_large: { en: "Extra large", hi: "बहुत बड़ा" },
  high: { en: "High", hi: "उच्च" },
  voice: { en: "Voice", hi: "आवाज़" },
  touch: { en: "Touch", hi: "स्पर्श" },
  hybrid: { en: "Voice and touch", hi: "आवाज़ और स्पर्श" },
  text: { en: "Typing", hi: "लिखकर" },
  recommended: { en: "Recommended for you", hi: "आपके लिए सुझाया गया" },
  customized: { en: "Chosen by you", hi: "आपके द्वारा चुना गया" },

  // --- Visit -------------------------------------------------------------
  draft: { en: "Not started", hi: "शुरू नहीं हुआ" },
  in_progress: { en: "In progress", hi: "चल रहा है" },
  awaiting_review: { en: "Awaiting your review", hi: "आपकी समीक्षा की प्रतीक्षा" },
  cancelled: { en: "Cancelled", hi: "रद्द" },
  confirmed: { en: "Confirmed", hi: "पुष्ट" },
  routine: { en: "Routine", hi: "सामान्य" },
  priority: { en: "Priority", hi: "प्राथमिकता" },
  urgent: { en: "Urgent", hi: "तत्काल" },
  first_visit: { en: "First visit", hi: "पहली मुलाक़ात" },
  follow_up: { en: "Follow-up visit", hi: "अनुवर्ती मुलाक़ात" },

  // --- Clinical provenance ----------------------------------------------
  patient: { en: "You told us", hi: "आपने बताया" },
  document: { en: "From a document", hi: "दस्तावेज़ से" },
  previous_record: { en: "From an earlier visit", hi: "पिछली मुलाक़ात से" },
  clinician: { en: "From a clinician", hi: "चिकित्सक से" },

  // --- Findings ----------------------------------------------------------
  diagnosis: { en: "Condition", hi: "स्थिति" },
  medication: { en: "Medicine", hi: "दवा" },
  investigation: { en: "Test", hi: "जाँच" },
  procedure: { en: "Procedure", hi: "प्रक्रिया" },
  surgery: { en: "Surgery", hi: "ऑपरेशन" },
  allergy: { en: "Allergy", hi: "एलर्जी" },
  vital: { en: "Vital sign", hi: "जीवन संकेत" },
  note: { en: "Note", hi: "टिप्पणी" },
  visit: { en: "Visit", hi: "मुलाक़ात" },
  low: { en: "Low", hi: "कम" },
  unclear: { en: "Unclear", hi: "अस्पष्ट" },
  unreviewed: { en: "Not reviewed", hi: "समीक्षा नहीं हुई" },
  accepted: { en: "Kept", hi: "रखा गया" },
  rejected: { en: "Removed", hi: "हटाया गया" },

  // --- Care system -------------------------------------------------------
  allopathy: { en: "Allopathy", hi: "एलोपैथी" },
  ayurveda: { en: "Ayurveda", hi: "आयुर्वेद" },
  homoeopathy: { en: "Homoeopathy", hi: "होम्योपैथी" },
  unani: { en: "Unani", hi: "यूनानी" },
  siddha: { en: "Siddha", hi: "सिद्ध" },
  yoga_naturopathy: { en: "Yoga and Naturopathy", hi: "योग और प्राकृतिक चिकित्सा" },
  unsure: { en: "Not sure yet", hi: "अभी तय नहीं" },

  // --- Timeline provenance (composed with a document name) --------------
  uploaded_document: { en: "Document you uploaded", hi: "आपके द्वारा अपलोड किया दस्तावेज़" },
  visit_record: { en: "Visit record", hi: "मुलाक़ात का रिकॉर्ड" },
  understood_from_speech: {
    en: "Understood from what you said",
    hi: "आपने जो कहा उससे समझा गया",
  },
} as const satisfies Record<string, Translations>;

export type EnumValue = keyof typeof ENUM_LABELS;

/**
 * The label for an API enum value. An unmapped value degrades to a readable
 * slug rather than disappearing — a missing label should look untranslated,
 * never blank.
 */
export function enumLabel(value: string | null | undefined, language: Language): string {
  if (!value) return "";
  const entry = (ENUM_LABELS as Record<string, Translations | undefined>)[value];
  if (!entry) return value.replace(/_/g, " ");
  return localised(withOverlay(entry, language), language);
}

/**
 * Where a timeline entry came from, as a sentence. `found_in_document` needs
 * the document's name inside the sentence, which no flat label can express.
 */
export function sourceSentence(
  kind: string,
  name: string,
  language: Language,
): string {
  if (kind === "found_in_document") {
    return translate("timelineFoundIn", language).replace("{name}", name);
  }
  return enumLabel(kind, language);
}

/** Which enum labels are missing a translation. Used by the audit test. */
export function untranslatedLabels(language: Language): EnumValue[] {
  return (Object.keys(ENUM_LABELS) as EnumValue[]).filter(
    (key) => !withOverlay(ENUM_LABELS[key], language)[language],
  );
}

/**
 * Lab flags, shared by the document card and the timeline so the two views
 * can never disagree. Only flags derived from a printed reference range are
 * ever shown, and never as a diagnosis.
 */
export const LAB_FLAG_TONE: Record<LabFlag, "success" | "warning" | "neutral"> = {
  normal: "success",
  low: "warning",
  high: "warning",
  unclear: "neutral",
};

const LAB_FLAG_KEYS = {
  normal: "labNormal",
  low: "labLow",
  high: "labHigh",
  unclear: "labUnclear",
} as const;

export function labFlagLabel(flag: LabFlag, language: Language): string {
  return translate(LAB_FLAG_KEYS[flag], language);
}
