"""Domain enumerations shared by models, schemas and the rule engine.

These are plain `str` enums so they serialise directly to JSON and can be
mirrored one-for-one by the frontend TypeScript union types.
"""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:  # pragma: no cover - convenience only
        return self.value


# --- Patient ---------------------------------------------------------------
class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNDISCLOSED = "undisclosed"


class Language(StrEnum):
    """Supported interface languages.

    Every localised string is keyed off this enum. Adding a language here
    makes it selectable immediately; strings without a translation resolve
    through `app.shared.i18n.FALLBACK_CHAIN` rather than breaking.
    """

    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"
    TAMIL = "ta"
    GUJARATI = "gu"
    PUNJABI = "pa"


class OnboardingStatus(StrEnum):
    """Where a patient is in the first-time journey.

    Drives post-login routing, so a patient always resumes where they stopped.
    """

    # A patient row exists as soon as they authenticate; the name and the rest
    # of the profile arrive step by step after that.
    ABHA_PENDING = "abha_pending"
    PERSONAL_INFO_PENDING = "personal_info_pending"
    ASSESSMENT_PENDING = "assessment_pending"
    PREFERENCES_PENDING = "preferences_pending"
    CONSENT_PENDING = "consent_pending"
    MEDICAL_PROFILE_PENDING = "medical_profile_pending"
    COMPLETED = "completed"


# Canonical order of the onboarding journey, used for routing and progress.
ONBOARDING_SEQUENCE: tuple[OnboardingStatus, ...] = (
    OnboardingStatus.ABHA_PENDING,
    OnboardingStatus.PERSONAL_INFO_PENDING,
    OnboardingStatus.ASSESSMENT_PENDING,
    OnboardingStatus.PREFERENCES_PENDING,
    OnboardingStatus.CONSENT_PENDING,
    OnboardingStatus.MEDICAL_PROFILE_PENDING,
    OnboardingStatus.COMPLETED,
)


# --- ABHA ------------------------------------------------------------------
class AbhaVerificationStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    FAILED = "failed"
    SKIPPED = "skipped"


# --- Preferences -----------------------------------------------------------
class InterfaceMode(StrEnum):
    STANDARD = "standard"
    EASY = "easy"


class FontSize(StrEnum):
    NORMAL = "normal"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"


class ContrastMode(StrEnum):
    NORMAL = "normal"
    HIGH = "high"


class InteractionPreference(StrEnum):
    VOICE = "voice"
    TOUCH = "touch"
    HYBRID = "hybrid"


class PreferenceSource(StrEnum):
    """Whether the active preferences came from the engine or the patient."""

    RECOMMENDED = "recommended"
    CUSTOMIZED = "customized"


# --- Accessibility assessment ---------------------------------------------
class DigitalComfort(StrEnum):
    VERY_COMFORTABLE = "very_comfortable"
    SOMEWHAT_COMFORTABLE = "somewhat_comfortable"
    NEED_HELP = "need_help"
    PREFER_SIMPLE = "prefer_simple"


class PreferredInteraction(StrEnum):
    SPEAKING = "speaking"
    TOUCHING = "touching"
    BOTH = "both"


class DifficultyLevel(StrEnum):
    NONE = "none"
    SOMETIMES = "sometimes"
    YES = "yes"


class AccessibilityNeed(StrEnum):
    """Voluntarily disclosed needs. Never required, never inferred."""

    LOW_LITERACY = "low_literacy"
    LOW_VISION = "low_vision"
    HARD_OF_HEARING = "hard_of_hearing"
    LIMITED_HAND_MOBILITY = "limited_hand_mobility"
    NEEDS_ASSISTANT = "needs_assistant"
    PREFERS_SIGN_LANGUAGE = "prefers_sign_language"


# --- Consent ---------------------------------------------------------------
class ConsentPurpose(StrEnum):
    HEALTH_DATA_COLLECTION = "health_data_collection"
    SHARE_WITH_TREATING_DOCTOR = "share_with_treating_doctor"
    ABHA_LINKAGE = "abha_linkage"


class ConsentStatus(StrEnum):
    GRANTED = "granted"
    DECLINED = "declined"
    REVOKED = "revoked"


# --- Encounter -------------------------------------------------------------
class EncounterStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    AWAITING_REVIEW = "awaiting_review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EncounterPriority(StrEnum):
    ROUTINE = "routine"
    PRIORITY = "priority"
    URGENT = "urgent"


class VisitType(StrEnum):
    FIRST_VISIT = "first_visit"
    FOLLOW_UP = "follow_up"


# --- Documents -------------------------------------------------------------
class DocumentType(StrEnum):
    PRESCRIPTION = "prescription"
    LAB_REPORT = "lab_report"
    DISCHARGE_SUMMARY = "discharge_summary"
    OTHER = "other"


class ProcessingStatus(StrEnum):
    """Explicit lifecycle for long-running/optional steps. Failure is never
    represented by NULL alone."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


# --- Clinical data provenance ---------------------------------------------
class ClinicalSource(StrEnum):
    PATIENT = "patient"
    DOCUMENT = "document"
    PREVIOUS_RECORD = "previous_record"
    CLINICIAN = "clinician"


# --- Phase 2: interview ----------------------------------------------------
class InputMethod(StrEnum):
    """How an answer reached us. The conversation engine never branches on it."""

    VOICE = "voice"
    TEXT = "text"
    TOUCH = "touch"


class ConversationStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    AWAITING_REVIEW = "awaiting_review"
    CONFIRMED = "confirmed"
    ABANDONED = "abandoned"


class AnswerKind(StrEnum):
    """How a question is presented and validated."""

    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    FREE_TEXT = "free_text"
    LIST = "list"
    YES_NO = "yes_no"
    SCALE = "scale"
    NUMBER = "number"


# --- Phase 2: document intelligence ---------------------------------------
class ExtractedEntityType(StrEnum):
    DIAGNOSIS = "diagnosis"
    MEDICATION = "medication"
    INVESTIGATION = "investigation"
    PROCEDURE = "procedure"
    SURGERY = "surgery"
    ALLERGY = "allergy"
    VITAL = "vital"
    NOTE = "note"


class LabFlag(StrEnum):
    """Only ever derived from a printed reference range — never guessed."""

    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    UNCLEAR = "unclear"


class ReviewState(StrEnum):
    """Extracted data is a finding to review, never a confirmed diagnosis."""

    UNREVIEWED = "unreviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class TimelineEventType(StrEnum):
    DOCUMENT = "document"
    DIAGNOSIS = "diagnosis"
    MEDICATION = "medication"
    INVESTIGATION = "investigation"
    SURGERY = "surgery"
    VISIT = "visit"


# --- Phase 2: AYUSH --------------------------------------------------------
class AyushPariksha(StrEnum):
    """The ten-fold examination (Dashavidha Pariksha)."""

    PRAKRITI = "prakriti"
    VIKRITI = "vikriti"
    SARA = "sara"
    SAMHANANA = "samhanana"
    PRAMANA = "pramana"
    SATMYA = "satmya"
    SATTVA = "sattva"
    AHARA_SHAKTI = "ahara_shakti"
    VYAYAMA_SHAKTI = "vyayama_shakti"
    VAYA = "vaya"


# --- Phase 3: encounters and safety ---------------------------------------
class RedFlagStatus(StrEnum):
    """Whether an encounter is currently flagged for urgent attention."""

    NONE = "none"
    ACTIVE = "active"
    # Set only by a clinician in a later phase; a patient can never clear it.
    CLINICIAN_CLEARED = "clinician_cleared"


class RedFlagCategory(StrEnum):
    """Broad clinical categories. The *criteria* behind each are private."""

    BREATHING = "breathing"
    CHEST = "chest"
    BLEEDING = "bleeding"
    CONSCIOUSNESS = "consciousness"
    NEUROLOGICAL = "neurological"
    OTHER = "other"


class RedFlagSource(StrEnum):
    RULES = "rules"
    AI_ASSIST = "ai_assist"


class EncounterKind(StrEnum):
    """Which interview script an encounter session runs."""

    PROFILE = "profile"
    ENCOUNTER = "encounter"


class CareSystem(StrEnum):
    """Which system of medicine the patient is attending for.

    Drives how long the interview is: an allopathic visit asks about today
    only, while an Ayurvedic visit adds the Dashavidha and Ashtasthana
    examinations. Recorded per *encounter*, because a patient may attend an
    allopathic OPD one day and an AYUSH OPD the next.
    """

    ALLOPATHY = "allopathy"
    AYURVEDA = "ayurveda"
    HOMOEOPATHY = "homoeopathy"
    UNANI = "unani"
    SIDDHA = "siddha"
    YOGA_NATUROPATHY = "yoga_naturopathy"
    UNSURE = "unsure"


# Systems whose full examination framework this build implements.
FULLY_SUPPORTED_CARE_SYSTEMS: frozenset[CareSystem] = frozenset(
    {CareSystem.ALLOPATHY, CareSystem.AYURVEDA}
)

# AYUSH systems that share the diet/lifestyle enquiry but whose own
# examinations are not built. The UI says so rather than faking a
# questionnaire.
PARTIAL_AYUSH_SYSTEMS: frozenset[CareSystem] = frozenset(
    {
        CareSystem.HOMOEOPATHY,
        CareSystem.UNANI,
        CareSystem.SIDDHA,
        CareSystem.YOGA_NATUROPATHY,
    }
)


class AyushAshtasthana(StrEnum):
    """The eight-fold examination (Ashtasthana Pariksha)."""

    NADI = "nadi"
    MUTRA = "mutra"
    MALA = "mala"
    JIHVA = "jihva"
    SHABDA = "shabda"
    SPARSHA = "sparsha"
    DRIK = "drik"
    AKRITI = "akriti"
