"""AYUSH assessment use cases."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Any

from app.modules.ayush.content import (
    AHARA_OPTIONS,
    ASHTASTHANA,
    DASHAVIDHA,
    LIFESTYLE_FACTORS,
    TOTAL_AYUSH_FACTORS,
    VIHARA_OPTIONS,
    VALID_AHARA,
    VALID_ASHTASTHANA,
    VALID_ASHTASTHANA_OPTIONS,
    VALID_LIFESTYLE,
    VALID_LIFESTYLE_OPTIONS,
    VALID_OPTIONS,
    VALID_PARIKSHA,
    VALID_VIHARA,
)
from app.modules.ayush.models import AyushAssessment
from app.modules.patient.models import Patient
from app.shared.enums import Language
from app.shared.errors import ValidationFailedError
from app.shared.i18n import localise


_FIELD_VOCABULARY = {
    "dashavidha": (VALID_PARIKSHA, VALID_OPTIONS),
    "ashtasthana": (VALID_ASHTASTHANA, VALID_ASHTASTHANA_OPTIONS),
    "lifestyle": (VALID_LIFESTYLE, VALID_LIFESTYLE_OPTIONS),
}


def get(db: Session, patient: Patient) -> AyushAssessment | None:
    return db.scalar(
        select(AyushAssessment)
        .where(AyushAssessment.patient_id == patient.id)
        .order_by(AyushAssessment.created_at.desc())
        .limit(1)
    )


def save(
    db: Session,
    patient: Patient,
    *,
    dashavidha: dict[str, str],
    ahara: list[str],
    vihara: list[str],
    notes: str | None,
    ashtasthana: dict[str, str] | None = None,
    lifestyle: dict[str, str] | None = None,
) -> AyushAssessment:
    """Store the assessment, rejecting anything outside the known vocabulary.

    Partial answers are fine — the assessment is optional and a patient may
    skip individual factors — but an unrecognised key or value is a bug or a
    tampered request, not a patient choice.
    """
    unknown_keys = set(dashavidha) - VALID_PARIKSHA
    if unknown_keys:
        raise ValidationFailedError(
            f"Unknown assessment factor(s): {', '.join(sorted(unknown_keys))}"
        )
    for key, value in dashavidha.items():
        if value and value not in VALID_OPTIONS[key]:
            raise ValidationFailedError(f"'{value}' is not a valid answer for {key}.")

    for field, supplied in (("ashtasthana", ashtasthana or {}), ("lifestyle", lifestyle or {})):
        valid_keys, valid_options = _FIELD_VOCABULARY[field]
        unknown = set(supplied) - valid_keys
        if unknown:
            raise ValidationFailedError(
                f"Unknown {field} factor(s): {', '.join(sorted(unknown))}"
            )
        for key, value in supplied.items():
            if value and value not in valid_options[key]:
                raise ValidationFailedError(f"'{value}' is not a valid answer for {key}.")

    unknown_ahara = set(ahara) - VALID_AHARA
    unknown_vihara = set(vihara) - VALID_VIHARA
    if unknown_ahara or unknown_vihara:
        raise ValidationFailedError(
            "Unknown diet or routine option: "
            f"{', '.join(sorted(unknown_ahara | unknown_vihara))}"
        )

    assessment = get(db, patient)
    if assessment is None:
        assessment = AyushAssessment(patient_id=patient.id)
        db.add(assessment)

    assessment.dashavidha = {k: v for k, v in dashavidha.items() if v}
    assessment.ashtasthana = {k: v for k, v in (ashtasthana or {}).items() if v}
    assessment.lifestyle = {k: v for k, v in (lifestyle or {}).items() if v}
    assessment.ahara = list(dict.fromkeys(ahara))
    assessment.vihara = list(dict.fromkeys(vihara))
    assessment.notes = (notes or "").strip() or None
    # "Complete" means every factor was answered; a partial record is valid.
    assessment.is_complete = len(assessment.dashavidha) == len(VALID_PARIKSHA)
    db.flush()
    return assessment


# --- Recording answers from inside a visit --------------------------------



def ensure(db: Session, patient: Patient) -> AyushAssessment:
    assessment = get(db, patient)
    if assessment is None:
        assessment = AyushAssessment(patient_id=patient.id)
        db.add(assessment)
        db.flush()
    return assessment


def record_answer(
    db: Session, patient: Patient, field: str, key: str, values: list[str]
) -> AyushAssessment:
    """Store one AYUSH answer given during a visit.

    Values outside the published vocabulary are dropped rather than stored:
    the option lists are served by the API, so anything else is a tampered
    request, not a patient choice.
    """
    assessment = ensure(db, patient)

    if field in _FIELD_VOCABULARY:
        valid_keys, valid_options = _FIELD_VOCABULARY[field]
        if key not in valid_keys or not values:
            return assessment
        value = values[0]
        if value not in valid_options[key]:
            return assessment
        # Reassign so SQLAlchemy notices the JSONB change.
        current = dict(getattr(assessment, field))
        current[key] = value
        setattr(assessment, field, current)

    elif field in ("ahara", "vihara"):
        allowed = VALID_AHARA if field == "ahara" else VALID_VIHARA
        accepted = [value for value in values if value in allowed]
        if not accepted:
            return assessment
        setattr(assessment, field, list(dict.fromkeys(accepted)))
    else:
        return assessment

    assessment.is_complete = len(assessment.dashavidha) == len(VALID_PARIKSHA)
    db.flush()
    return assessment


def recorded_for_review(
    assessment: AyushAssessment | None, language: Language | str
) -> dict[str, Any] | None:
    """What the patient answered, worded for the review screen.

    An Ayurvedic visit asks around twenty more questions than an allopathic
    one, and those answers go to the assessment rather than to the medical
    profile — so without this the patient reaches the review screen having
    answered thirty-three questions and sees five, which reads as if their
    answers were lost.

    Values are looked up back through the question content, so the screen
    shows the words the patient chose, not the stored vocabulary key.
    """
    if assessment is None:
        return None

    def labels(factors: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        return {factor["key"]: factor for factor in factors}

    def entries(
        stored: dict[str, str], factors: list[dict[str, Any]], group: str
    ) -> list[dict[str, str]]:
        index = labels(factors)
        rows = []
        for key, value in (stored or {}).items():
            factor = index.get(key)
            if factor is None:
                continue
            option = next(
                (o for o in factor["options"] if o["value"] == value), None
            )
            rows.append(
                {
                    "group": group,
                    "term": localise(factor["term"], language),
                    "question": localise(factor["prompt"], language),
                    "answer": localise(option["label"], language) if option else value,
                }
            )
        return rows

    def chosen(values: list[str], options: list[dict[str, Any]], group: str) -> list[dict[str, str]]:
        index = {option["value"]: option for option in options}
        return [
            {
                "group": group,
                "term": "",
                "question": "",
                "answer": localise(index[value]["label"], language),
            }
            for value in (values or [])
            if value in index
        ]

    rows = [
        *entries(assessment.dashavidha, DASHAVIDHA, "dashavidha"),
        *entries(assessment.ashtasthana, ASHTASTHANA, "ashtasthana"),
        *entries(assessment.lifestyle, LIFESTYLE_FACTORS, "lifestyle"),
        *chosen(assessment.ahara, AHARA_OPTIONS, "ahara"),
        *chosen(assessment.vihara, VIHARA_OPTIONS, "vihara"),
    ]
    return {
        "count": assessment.answered_count,
        "total": TOTAL_AYUSH_FACTORS,
        "entries": rows,
    }
