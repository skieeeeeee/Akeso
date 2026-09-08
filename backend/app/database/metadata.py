"""Single import point that registers every model with the metadata.

Alembic autogenerate and the test bootstrap both import this, so adding a
model means adding one line here — nothing else needs to know.
"""

from app.database.base import Base
from app.modules.abha.models import AbhaProfile
from app.modules.accessibility.models import (
    AccessibilityAssessment,
    PatientPreferences,
)
from app.modules.auth.models import OtpChallenge
from app.modules.consent.models import Consent
from app.modules.ayush.models import AyushAssessment
from app.modules.documents.models import Document, ExtractedMedicalData
from app.modules.interview.models import ConversationAnswer, ConversationSession
from app.modules.encounter.models import Encounter
from app.modules.medical_history.models import MedicalProfile
from app.modules.patient.models import Patient
from app.modules.red_flags.models import RedFlag

__all__ = [
    "Base",
    "AbhaProfile",
    "AccessibilityAssessment",
    "PatientPreferences",
    "OtpChallenge",
    "Consent",
    "AyushAssessment",
    "ConversationAnswer",
    "ConversationSession",
    "Document",
    "ExtractedMedicalData",
    "Encounter",
    "MedicalProfile",
    "Patient",
    "RedFlag",
]
