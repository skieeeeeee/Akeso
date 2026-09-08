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

import logging

import httpx

from app.config import settings

log = logging.getLogger("medikiosk.speech")

_API = "https://api.elevenlabs.io/v1/text-to-speech"

# Long enough for a question and its help text; a whole page is not a use case
# here and would only run up someone's character quota.
MAX_CHARACTERS = 600


class SpeechUnavailable(RuntimeError):
    """No audio could be produced. The caller falls back to the browser."""


async def synthesise(text: str, language: str) -> bytes:
    """Speak `text`, returning MP3 bytes.

    @param language a `Language` value; ElevenLabs detects the language from
                    the text itself, so this only tags the request for logs.
    @raises SpeechUnavailable when speech is switched off, the text is empty,
            or the upstream call fails. Never raises anything else: audio is
            an enhancement and must not be able to break a page.
    """
    if not settings.elevenlabs_api_key:
        raise SpeechUnavailable("Speech is not configured on this server.")

    spoken = " ".join(text.split())[:MAX_CHARACTERS]
    if not spoken:
        raise SpeechUnavailable("There was nothing to read out.")

    url = f"{_API}/{settings.elevenlabs_voice_id}"
    try:
        async with httpx.AsyncClient(
            timeout=settings.elevenlabs_timeout_seconds
        ) as client:
            response = await client.post(
                url,
                headers={
                    "xi-api-key": settings.elevenlabs_api_key,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                json={
                    "text": spoken,
                    "model_id": settings.elevenlabs_model,
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                },
            )
    except httpx.HTTPError as exc:
        log.warning("speech request failed (%s): %s", language, exc)
        raise SpeechUnavailable("We could not reach the speech service.") from exc

    if response.status_code != 200:
        # Quota, a bad key and a bad voice id all mean the same thing to the
        # caller: read it in the browser instead.
        log.warning(
            "speech returned %s for %s: %s",
            response.status_code,
            language,
            response.text[:200],
        )
        raise SpeechUnavailable("The speech service did not return audio.")

    audio = response.content
    if not audio:
        raise SpeechUnavailable("The speech service returned no audio.")
    return audio
