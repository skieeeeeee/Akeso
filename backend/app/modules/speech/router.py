"""Reading text aloud for the patient.

One endpoint, deliberately small. It exists so the ElevenLabs key stays on
the server; the browser sends text and gets audio back.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from pydantic import Field

from app.modules.auth.dependencies import current_patient
from app.modules.patient.models import Patient
from app.services.speech import MAX_CHARACTERS, SpeechUnavailable, probe, synthesise
from app.shared.enums import Language
from app.shared.errors import UpstreamUnavailableError
from app.shared.schemas import ApiModel

router = APIRouter(prefix="/speech", tags=["speech"])


class SpeechIn(ApiModel):
    text: str = Field(min_length=1, max_length=MAX_CHARACTERS)
    # Tags the request; ElevenLabs detects the language from the text itself.
    language: Language = Language.ENGLISH


class SpeechStatusOut(ApiModel):
    """Whether the server can speak, so the client knows before it asks."""

    available: bool


@router.get("/status", response_model=SpeechStatusOut)
def status() -> SpeechStatusOut:
    from app.config import settings

    return SpeechStatusOut(available=settings.speech_enabled)


@router.get("/diagnostics")
async def diagnostics(patient: Patient = Depends(current_patient)) -> dict:
    """Prove whether this deployment can really speak, and if not, why.

    `/status` above only reports whether a key is set. It stayed true on a
    deployment where every request failed, because the configured voice was
    a shared library voice the free plan may not use — a 402 that looks
    identical, from outside, to a bad key or an exhausted quota.

    Signed-in only, spends one very short synthesis, and never returns the
    API key.
    """
    return await probe()


@router.post(
    "",
    responses={200: {"content": {"audio/mpeg": {}}}},
    response_class=Response,
)
async def speak(
    payload: SpeechIn,
    patient: Patient = Depends(current_patient),
) -> Response:
    """Return spoken audio for a short piece of text.

    Requires a signed-in patient: this spends a character quota, so it is not
    left open to anyone who finds the URL.

    @raises UpstreamUnavailableError when speech is off or upstream failed —
            the client then reads the text with the browser's own voice, so a
            503 here is never a dead end.
    """
    try:
        audio = await synthesise(payload.text, payload.language.value)
    except SpeechUnavailable as exc:
        raise UpstreamUnavailableError(str(exc)) from exc

    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={
            # Same text and voice give the same audio, so let the browser
            # keep it rather than spending the quota twice.
            "Cache-Control": "private, max-age=3600",
        },
    )
