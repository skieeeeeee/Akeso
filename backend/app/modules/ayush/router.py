"""AYUSH endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.ayush import service
from app.modules.ayush.content import (
    AHARA_OPTIONS,
    ASHTASTHANA,
    DASHAVIDHA,
    INTRO,
    LIFESTYLE_FACTORS,
    TOTAL_AYUSH_FACTORS,
    VIHARA_OPTIONS,
)
from app.modules.patient.models import Patient
from app.shared.schemas import ApiModel

router = APIRouter(prefix="/ayush", tags=["ayush"])


class AyushContentOut(ApiModel):
    intro: dict[str, Any]
    dashavidha: list[dict[str, Any]]
    # The eight-fold examination; a practitioner confirms each at the couch.
    ashtasthana: list[dict[str, Any]]
    # Agni/Koshtha, Nidra, Manas.
    lifestyle: list[dict[str, Any]]
    ahara_options: list[dict[str, Any]]
    vihara_options: list[dict[str, Any]]
    # How many factors a full Ayurvedic intake covers.
    total_factors: int


class AyushIn(ApiModel):
    # Partial submissions are expected: every factor is skippable.
    dashavidha: dict[str, str] = Field(default_factory=dict)
    ashtasthana: dict[str, str] = Field(default_factory=dict)
    lifestyle: dict[str, str] = Field(default_factory=dict)
    ahara: list[str] = Field(default_factory=list)
    vihara: list[str] = Field(default_factory=list)
    notes: str | None = Field(default=None, max_length=2000)


class AyushOut(ApiModel):
    dashavidha: dict[str, str]
    ashtasthana: dict[str, str]
    lifestyle: dict[str, str]
    ahara: list[str]
    vihara: list[str]
    notes: str | None
    is_complete: bool
    answered_count: int


@router.get("/content", response_model=AyushContentOut)
def content() -> AyushContentOut:
    """The Dashavidha, Ahara and Vihara questions, in every language."""
    return AyushContentOut(
        intro=INTRO,
        dashavidha=DASHAVIDHA,
        ashtasthana=ASHTASTHANA,
        lifestyle=LIFESTYLE_FACTORS,
        ahara_options=AHARA_OPTIONS,
        vihara_options=VIHARA_OPTIONS,
        total_factors=TOTAL_AYUSH_FACTORS,
    )


@router.get("", response_model=AyushOut | None)
def read(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> AyushOut | None:
    assessment = service.get(db, patient)
    return AyushOut.model_validate(assessment) if assessment else None


@router.put("", response_model=AyushOut)
def save(
    payload: AyushIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> AyushOut:
    assessment = service.save(
        db,
        patient,
        dashavidha=payload.dashavidha,
        ashtasthana=payload.ashtasthana,
        lifestyle=payload.lifestyle,
        ahara=payload.ahara,
        vihara=payload.vihara,
        notes=payload.notes,
    )
    return AyushOut.model_validate(assessment)
