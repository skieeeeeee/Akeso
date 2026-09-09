"""ElevenLabs text to speech, proxied so the key stays on the server.

Why this exists at all: a phone or kiosk commonly has no installed voice for
Marathi, Gujarati or Punjabi, so the browser silently cannot read a question
aloud in those languages — which is precisely the patient who most needs it
read aloud.

Why it is a proxy: a Vite build inlines every variable it can see, so a key
handed to the client would be readable by any visitor. The browser calls our
own endpoint instead, and the key never leaves the server.
"""

from __future__ import annotations

import asyncio
import logging

import httpx

from app.config import settings

log = logging.getLogger("medikiosk.speech")

_API = "https://api.elevenlabs.io/v1/text-to-speech"

# Long enough for a question and its help text; a whole page is not a use case
# here and would only run up someone's character quota.
MAX_CHARACTERS = 600

# Worth retrying. A free ElevenLabs plan allows four concurrent requests, so a
# patient moving quickly through questions — or a couple of kiosks in one
# clinic — hits 429 with nothing wrong at all. The AI provider has retried
# these from the start; speech did not, and every rejection fell through to a
# browser voice that does not exist for Marathi, Gujarati or Punjabi. So the
# patient pressed listen and heard silence.
_RETRYABLE = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 3
_RETRY_BASE_DELAY = 0.8


class SpeechUnavailable(RuntimeError):
    """No audio could be produced. The caller falls back to the browser.

    `str(exc)` is what the patient's client sees, so it stays plain. The
    other three describe the upstream failure and exist only so `probe` can
    report which failure it was; they are never sent to a patient.
    """

    def __init__(
        self,
        message: str,
        *,
        reason: str = "upstream_error",
        http_status: int | None = None,
        technical: str | None = None,
    ) -> None:
        super().__init__(message)
        self.reason = reason
        self.http_status = http_status
        self.technical = technical


# Named so an operator reading a probe result does not have to look up what
# ElevenLabs means by each status code.
_REASONS = {
    401: "bad_key_or_missing_permission",
    402: "paid_plan_required",
    403: "forbidden",
    404: "voice_not_found",
    422: "bad_request",
    429: "quota_or_rate_limit",
}


async def probe() -> dict[str, object]:
    """Say whether speech actually works right now, and if not, why.

    `synthesise` deliberately collapses every failure into one message,
    because its caller does the same thing regardless: read the text with the
    browser voice. That is right for the patient and useless for an operator
    — a deployment can report `available: true` and fail every request, with
    no way to tell a key without the text_to_speech permission from a voice
    the plan may not use. This is the missing half.

    @returns {ok, reason, http_status, detail, voice_id, model} — detail is a
             short upstream snippet, never the API key.
    """
    base: dict[str, object] = {
        "voice_id": settings.elevenlabs_voice_id,
        "model": settings.elevenlabs_model,
        "key_present": bool(settings.elevenlabs_api_key),
    }
    if not settings.elevenlabs_api_key:
        return {
            **base,
            "ok": False,
            "reason": "not_configured",
            "http_status": None,
            "detail": "ELEVENLABS_API_KEY is not set on this server.",
        }

    try:
        audio = await synthesise("ok", "en")
    except SpeechUnavailable as exc:
        return {
            **base,
            "ok": False,
            "reason": exc.reason,
            "http_status": exc.http_status,
            "detail": exc.technical or str(exc),
        }
    return {
        **base,
        "ok": True,
        "reason": None,
        "http_status": 200,
        "detail": f"{len(audio)} bytes of audio",
    }


async def synthesise(text: str, language: str) -> bytes:
    """Speak `text`, returning MP3 bytes.

    @param language a `Language` value; ElevenLabs detects the language from
                    the text itself, so this only tags the request for logs.
    @raises SpeechUnavailable when speech is switched off, the text is empty,
            or the upstream call fails. Never raises anything else: audio is
            an enhancement and must not be able to break a page.
    """
    if not settings.elevenlabs_api_key:
        raise SpeechUnavailable(
            "Speech is not configured on this server.", reason="not_configured"
        )

    spoken = " ".join(text.split())[:MAX_CHARACTERS]
    if not spoken:
        raise SpeechUnavailable("There was nothing to read out.", reason="empty_text")

    url = f"{_API}/{settings.elevenlabs_voice_id}"
    payload = {
        "text": spoken,
        "model_id": settings.elevenlabs_model,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
    }
    headers = {
        "xi-api-key": settings.elevenlabs_api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    delay = _RETRY_BASE_DELAY
    response: httpx.Response | None = None
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            async with httpx.AsyncClient(
                timeout=settings.elevenlabs_timeout_seconds
            ) as client:
                response = await client.post(url, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            log.warning("speech request failed (%s, attempt %s): %s", language, attempt, exc)
            if attempt == _MAX_ATTEMPTS:
                raise SpeechUnavailable(
                    "We could not reach the speech service.",
                    reason="unreachable",
                    technical=str(exc)[:200],
                ) from exc
        else:
            if response.status_code == 200:
                break
            if response.status_code not in _RETRYABLE or attempt == _MAX_ATTEMPTS:
                break
            log.info(
                "speech returned %s, retrying in %.1fs (attempt %s/%s)",
                response.status_code,
                delay,
                attempt,
                _MAX_ATTEMPTS,
            )
        await asyncio.sleep(delay)
        delay *= 2

    assert response is not None  # every other path raised
    if response.status_code != 200:
        # Quota, a bad key and a bad voice id all mean the same thing to the
        # caller: read it in the browser instead. The distinction still gets
        # recorded, because it is the only thing that tells an operator which
        # of those three it was.
        log.warning(
            "speech returned %s for %s: %s",
            response.status_code,
            language,
            response.text[:200],
        )
        raise SpeechUnavailable(
            "The speech service did not return audio.",
            reason=_REASONS.get(response.status_code, "upstream_error"),
            http_status=response.status_code,
            technical=response.text[:300],
        )

    audio = response.content
    if not audio:
        raise SpeechUnavailable(
            "The speech service returned no audio.", reason="empty_audio", http_status=200
        )
    return audio
