"""Interview endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import current_patient
from app.modules.interview import service
from app.modules.interview.schemas import (
    AnswerIn,
    AnswerRecord,
    InterviewView,
    StartInterviewIn,
    TranscriptView,
)
from app.modules.patient.models import Patient
from app.services.ai import provider_status

router = APIRouter(prefix="/interview", tags=["interview"])


@router.get("/ai-status")
def ai_status() -> dict:
    """Whether AI assistance is active. The UI explains this to the patient."""
    return provider_status()


@router.post("/start", response_model=InterviewView)
def start(
    payload: StartInterviewIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> InterviewView:
    """Begin the medical interview, or resume one already in progress."""
    session = service.start(db, patient, payload)
    return service.view(db, session, patient)


@router.get("/current", response_model=InterviewView | None)
def current(
    patient: Patient = Depends(current_patient), db: Session = Depends(get_db)
) -> InterviewView | None:
    session = service.active_session(db, patient)
    return service.view(db, session, patient) if session else None


@router.get("/{session_id}", response_model=InterviewView)
def get_session(
    session_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> InterviewView:
    """The current question without changing anything (safe on reload)."""
    return service.view(db, service.get(db, patient, session_id), patient)


@router.post("/{session_id}/answer", response_model=InterviewView)
async def answer(
    session_id: uuid.UUID,
    payload: AnswerIn,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> InterviewView:
    """Record one answer, whatever input method produced it."""
    return await service.answer(db, patient, session_id, payload)


@router.post("/{session_id}/back", response_model=InterviewView)
def back(
    session_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> InterviewView:
    """Reopen the previous question so the answer can be changed."""
    return service.back(db, patient, session_id)


@router.get("/{session_id}/transcript", response_model=TranscriptView)
def transcript(
    session_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> TranscriptView:
    answers = service.transcript(db, patient, session_id)
    return TranscriptView(
        session_id=session_id,
        answers=[AnswerRecord.model_validate(row) for row in answers],
    )


@router.post("/{session_id}/confirm", response_model=InterviewView)
def confirm(
    session_id: uuid.UUID,
    patient: Patient = Depends(current_patient),
    db: Session = Depends(get_db),
) -> InterviewView:
    """Patient confirms the interview after reviewing it."""
    session = service.confirm(db, patient, session_id)
    return service.view(db, session, patient)
