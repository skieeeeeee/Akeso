"""Fictional demo patients.

ALL medical information here is invented for demonstration. No real person,
ABHA number or medical record is represented.

Definitions live beside the patient module (rather than in the seed script)
because both the seeder and the demo sign-in endpoint need them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from app.shared.enums import (
    AccessibilityNeed,
    ConsentPurpose,
    DifficultyLevel,
    DigitalComfort,
    Gender,
    Language,
    OnboardingStatus,
    PreferredInteraction,
)
from app.shared.i18n import Localised, t


@dataclass(frozen=True, slots=True)
class DemoAssessment:
    digital_comfort: DigitalComfort
    preferred_interaction: PreferredInteraction
    reading_difficulty: DifficultyLevel
    hearing_difficulty: DifficultyLevel
    vision_difficulty: DifficultyLevel
    additional_needs: tuple[AccessibilityNeed, ...] = ()


@dataclass(frozen=True, slots=True)
class DemoVisit:
    """A previous, submitted visit — what makes a patient "returning"."""

    complaint: str
    days_ago: int
    detail: str = ""
    was_urgent: bool = False


@dataclass(frozen=True, slots=True)
class DemoDocument:
    """A record on file, with text the OCR layer can actually read."""

    title: str
    document_type: str
    text: str


@dataclass(frozen=True, slots=True)
class DemoPatientDefinition:
    demo_key: str
    # Localised: the demo picker sits on the sign-in screen, before a patient
    # has a stored language, so it follows the interface language.
    label: Localised
    description: Localised
    mobile_number: str
    full_name: str
    date_of_birth: date
    gender: Gender
    language: Language
    onboarding_status: OnboardingStatus
    abha_id: str | None = None
    assessment: DemoAssessment | None = None
    consents: tuple[ConsentPurpose, ...] = ()
    emergency_contact: tuple[str, str, str] | None = None
    medical: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    visits: tuple[DemoVisit, ...] = ()
    documents: tuple[DemoDocument, ...] = ()


DEMO_PATIENTS: dict[str, DemoPatientDefinition] = {
    # --- 1. Returning patient, standard preferences ------------------------
    "standard": DemoPatientDefinition(
        demo_key="standard",
        label=t("Rajesh Kumar · 52", "राजेश कुमार · 52"),
        description=t(
            "Returning patient, comfortable with digital forms. Standard mode.",
            "पुराने मरीज़, डिजिटल फ़ॉर्म में सहज। मानक मोड।",
        ),
        mobile_number="9812340001",
        full_name="Rajesh Kumar",
        date_of_birth=date(1974, 3, 15),
        gender=Gender.MALE,
        language=Language.ENGLISH,
        onboarding_status=OnboardingStatus.COMPLETED,
        abha_id="12-3456-7890-0001",
        assessment=DemoAssessment(
            digital_comfort=DigitalComfort.VERY_COMFORTABLE,
            preferred_interaction=PreferredInteraction.TOUCHING,
            reading_difficulty=DifficultyLevel.NONE,
            hearing_difficulty=DifficultyLevel.NONE,
            vision_difficulty=DifficultyLevel.NONE,
        ),
        consents=(
            ConsentPurpose.HEALTH_DATA_COLLECTION,
            ConsentPurpose.SHARE_WITH_TREATING_DOCTOR,
            ConsentPurpose.ABHA_LINKAGE,
        ),
        emergency_contact=("Sunita Kumar", "9812340091", "Spouse"),
        medical={
            "past_medical_history": [
                {"value": "Type 2 diabetes mellitus", "note": "Diagnosed 2019"},
                {"value": "Hypertension", "note": "Diagnosed 2021"},
            ],
            "current_medications": [
                {"value": "Metformin", "dose": "500 mg", "frequency": "Twice daily"},
                {"value": "Telmisartan", "dose": "40 mg", "frequency": "Once daily"},
            ],
            "allergies": [{"value": "Sulfa drugs", "note": "Rash"}],
            "surgical_history": [{"value": "Appendicectomy", "note": "2005"}],
            "family_history": [{"value": "Father had diabetes"}],
            "personal_history": [
                {"value": "Non-smoker"},
                {"value": "Vegetarian diet"},
            ],
            "previous_investigations": [
                {"value": "HbA1c 8.4%", "note": "March 2026"},
                {"value": "Haemoglobin 10.2 g/dL", "note": "March 2026"},
            ],
        },
        visits=(
            DemoVisit(
                complaint="Routine diabetes review",
                days_ago=94,
                detail="Feeling generally well, wanted sugar levels checked",
            ),
            DemoVisit(
                complaint="Burning feet at night",
                days_ago=31,
                detail="Worse after walking, both feet",
            ),
        ),
        documents=(
            DemoDocument(
                title="Dr Mehta prescription",
                document_type="prescription",
                text=(
                    "SHRI SAI POLYCLINIC\n"
                    "Dr. A. R. Mehta, MBBS MD (Medicine)\n"
                    "Date: 12/03/2026\n"
                    "Diagnosis: Type 2 Diabetes Mellitus, Hypertension\n"
                    "Rx\n"
                    "1. Tab. Metformin 500 mg  BD  x 30 days\n"
                    "2. Tab. Telmisartan 40 mg  OD  x 30 days\n"
                    "3. Tab. Atorvastatin 10 mg  HS  x 30 days\n"
                    "Advice: Low salt diet, 30 min walk daily\n"
                    "Note: Allergic to Sulfa drugs\n"
                ),
            ),
            DemoDocument(
                title="City Lab blood report",
                document_type="lab_report",
                text=(
                    "CITY DIAGNOSTIC LABORATORY\n"
                    "NABL Accredited\n"
                    "Collected on: 10/03/2026\n"
                    "Haemoglobin 10.2 g/dL (13.0-17.0)\n"
                    "Total Leucocyte Count 11800 /uL (4000-11000)\n"
                    "Fasting Blood Sugar 168 mg/dL (70-100)\n"
                    "HbA1c 8.4 % (4.0-5.6)\n"
                    "Serum Creatinine 1.1 mg/dL (0.7-1.3)\n"
                    "Remarks: Anaemia with poor glycaemic control\n"
                ),
            ),
        ),
    ),
    # --- 2. Easy Mode recommended -----------------------------------------
    "easy": DemoPatientDefinition(
        demo_key="easy",
        label=t("Kamla Devi · 71", "कमला देवी · 71"),
        description=t(
            "Prefers a simpler experience. Easy mode with audio guidance.",
            "आसान अनुभव पसंद करती हैं। आवाज़ मार्गदर्शन के साथ आसान मोड।",
        ),
        mobile_number="9812340002",
        full_name="कमला देवी",
        date_of_birth=date(1955, 7, 9),
        gender=Gender.FEMALE,
        language=Language.HINDI,
        onboarding_status=OnboardingStatus.COMPLETED,
        abha_id="12-3456-7890-0002",
        assessment=DemoAssessment(
            digital_comfort=DigitalComfort.PREFER_SIMPLE,
            preferred_interaction=PreferredInteraction.SPEAKING,
            reading_difficulty=DifficultyLevel.SOMETIMES,
            hearing_difficulty=DifficultyLevel.NONE,
            vision_difficulty=DifficultyLevel.NONE,
            additional_needs=(AccessibilityNeed.LOW_LITERACY,),
        ),
        consents=(
            ConsentPurpose.HEALTH_DATA_COLLECTION,
            ConsentPurpose.SHARE_WITH_TREATING_DOCTOR,
        ),
        emergency_contact=("रमेश प्रसाद", "9812340092", "बेटा"),
        medical={
            "past_medical_history": [
                {"value": "दोनों घुटनों में गठिया", "note": "2018 से"}
            ],
            "current_medications": [
                {"value": "कैल्शियम और विटामिन डी3", "frequency": "दिन में एक बार"}
            ],
            "allergies": [{"value": "कोई ज्ञात एलर्जी नहीं"}],
            "personal_history": [{"value": "परिवार के साथ रहती हैं"}],
        },
        visits=(
            DemoVisit(
                complaint="सीढ़ी चढ़ते समय घुटनों में दर्द",
                days_ago=58,
                detail="दोनों घुटने, सुबह ज़्यादा",
            ),
        ),
        documents=(
            DemoDocument(
                title="अस्थि रोग पर्चा",
                document_type="discharge_summary",
                text=(
                    "GOVERNMENT DISTRICT HOSPITAL\n"
                    "Orthopaedics Out-patient Note\n"
                    "Date: 11/01/2026\n"
                    "Diagnosis: Osteoarthritis of both knees\n"
                    "Rx\n"
                    "1. Tab. Paracetamol 650 mg  SOS  x 10 days\n"
                    "2. Tab. Calcium with Vitamin D3  OD  x 60 days\n"
                    "Advice: Quadriceps strengthening exercises\n"
                ),
            ),
        ),
    ),
    # --- 3. Visual accessibility preferences ------------------------------
    "low_vision": DemoPatientDefinition(
        demo_key="low_vision",
        label=t("Anil Sharma · 45", "अनिल शर्मा · 45"),
        description=t(
            "Low vision. Extra-large text and high contrast.",
            "कम दृष्टि। बहुत बड़ा टेक्स्ट और उच्च कंट्रास्ट।",
        ),
        mobile_number="9812340003",
        full_name="Anil Sharma",
        date_of_birth=date(1981, 11, 2),
        gender=Gender.MALE,
        language=Language.ENGLISH,
        onboarding_status=OnboardingStatus.COMPLETED,
        abha_id="12-3456-7890-0003",
        assessment=DemoAssessment(
            digital_comfort=DigitalComfort.SOMEWHAT_COMFORTABLE,
            preferred_interaction=PreferredInteraction.BOTH,
            reading_difficulty=DifficultyLevel.YES,
            hearing_difficulty=DifficultyLevel.NONE,
            vision_difficulty=DifficultyLevel.YES,
            additional_needs=(AccessibilityNeed.LOW_VISION,),
        ),
        consents=(
            ConsentPurpose.HEALTH_DATA_COLLECTION,
            ConsentPurpose.SHARE_WITH_TREATING_DOCTOR,
        ),
        emergency_contact=("Priya Sharma", "9812340093", "Spouse"),
        medical={
            "past_medical_history": [
                {"value": "Diabetic retinopathy", "note": "Both eyes, 2023"},
                {"value": "Type 2 diabetes mellitus", "note": "Diagnosed 2012"},
            ],
            "current_medications": [
                {"value": "Insulin glargine", "dose": "18 units", "frequency": "At night"},
                {"value": "Metformin", "dose": "1000 mg", "frequency": "Twice daily"},
            ],
            "allergies": [{"value": "No known allergies"}],
            "previous_investigations": [
                {"value": "Fasting blood sugar 168 mg/dL", "note": "February 2026"}
            ],
        },
        visits=(
            DemoVisit(
                complaint="Sudden blurring in the right eye",
                days_ago=12,
                detail="Came on over a day, no pain",
                was_urgent=True,
            ),
        ),
        documents=(
            DemoDocument(
                title="Retina clinic report",
                document_type="lab_report",
                text=(
                    "REGIONAL EYE INSTITUTE\n"
                    "Retina Clinic\n"
                    "Date: 26/08/2026\n"
                    "Diagnosis: Diabetic retinopathy, both eyes\n"
                    "HbA1c 9.1 % (4.0-5.6)\n"
                    "Advice: Strict glycaemic control, review in 3 months\n"
                ),
            ),
        ),
    ),
    # --- 4. First-time patient, onboarding incomplete ---------------------
    "incomplete": DemoPatientDefinition(
        demo_key="incomplete",
        label=t("Sunita Devi · 34", "सुनीता देवी · 34"),
        description=t(
            "First-time patient who stopped part-way through onboarding.",
            "पहली बार आई मरीज़, जिन्होंने पंजीकरण बीच में छोड़ा।",
        ),
        mobile_number="9812340004",
        full_name="सुनीता देवी",
        date_of_birth=date(1992, 5, 21),
        gender=Gender.FEMALE,
        language=Language.HINDI,
        # Stops right before the accessibility assessment.
        onboarding_status=OnboardingStatus.ASSESSMENT_PENDING,
        abha_id=None,
        assessment=None,
        consents=(),
        emergency_contact=None,
        medical={},
    ),
}


def demo_patient_list() -> list[DemoPatientDefinition]:
    return list(DEMO_PATIENTS.values())
