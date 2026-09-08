"""Text to speech.

Behind a provider boundary like every other outside service here: if it is
not configured, or it fails, the client falls back to the browser's own
speech synthesis and nothing about the interview changes.
"""

from app.services.speech.provider import (
    MAX_CHARACTERS,
    SpeechUnavailable,
    synthesise,
)

__all__ = ["MAX_CHARACTERS", "SpeechUnavailable", "synthesise"]
