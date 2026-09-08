"""AI provider abstraction.

Phase 1 deliberately ships NO AI functionality. What it ships is the seam:

* Feature code depends on the `AiProvider` protocol, never on a vendor SDK,
  so swapping Grok for another provider touches only this package.
* `NullProvider` is the configured default. It returns `None` for every call,
  which is the same signal a timeout or a validation failure produces — so
  feature code must already have a deterministic fallback path, and Phase 2
  cannot accidentally make the app depend on a model being reachable.
* `structured()` enforces the rule that model output is validated against a
  schema before it can reach the database or the UI. Raw text never flows
  through.
"""

from __future__ import annotations

from typing import Any, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel, ValidationError

import logging

from app.config import settings

log = logging.getLogger("medikiosk.ai")

TModel = TypeVar("TModel", bound=BaseModel)


class AiUnavailable(RuntimeError):
    """No provider is configured, or the configured one cannot be used."""


@runtime_checkable
class AiProvider(Protocol):
    """The only interface feature code may depend on."""

    name: str

    async def complete_json(
        self,
        *,
        system: str,
        prompt: str,
        max_tokens: int = 2048,
        image_base64: str | None = None,
        image_media_type: str = "image/png",
    ) -> dict[str, Any] | None:
        """Return parsed JSON, or None if the model could not be used.

        Implementations must never raise for an expected failure (timeout,
        rate limit, malformed output) — they return None so the caller falls
        back to its deterministic path.
        """
        ...


class NullProvider:
    """The Phase 1 default: no AI, always falls back."""

    name = "none"

    async def complete_json(
        self,
        *,
        system: str,
        prompt: str,
        max_tokens: int = 2048,
        image_base64: str | None = None,
        image_media_type: str = "image/png",
    ) -> dict[str, Any] | None:
        return None


def get_provider() -> AiProvider:
    """Resolve the configured provider.

    A provider name we do not implement fails loudly rather than silently
    behaving like `none`, so a misconfiguration cannot look like a working
    integration. A *configured but keyless* Grok falls back to `none` with a
    warning, because that is a deployment state, not a programming error.
    """
    configured = (settings.ai_provider or "none").lower()
    if configured in ("", "none"):
        return NullProvider()

    if configured == "grok":
        if not settings.ai_api_key:
            log.warning(
                "AI_PROVIDER=grok but AI_API_KEY is empty; using deterministic behaviour"
            )
            return NullProvider()
        from app.services.ai.grok_provider import GrokProvider

        return GrokProvider(
            api_key=settings.ai_api_key,
            model=settings.ai_model,
            base_url=settings.ai_base_url,
        )

    raise AiUnavailable(
        f"AI provider '{configured}' is not implemented in this build. "
        "Set AI_PROVIDER=none to use the deterministic behaviour."
    )


def provider_status() -> dict[str, Any]:
    """What the UI shows when explaining whether AI assistance is active."""
    try:
        provider = get_provider()
    except AiUnavailable as exc:
        return {"provider": "unavailable", "available": False, "detail": str(exc)}
    return {
        "provider": provider.name,
        "available": provider.name != "none",
        "detail": None,
    }


def structured(model: type[TModel], payload: dict[str, Any] | None) -> TModel | None:
    """Validate raw model output against a schema.

    @returns the parsed model, or None when the payload is missing or does
             not satisfy the schema. Never partially-valid data.
    """
    if payload is None:
        return None
    try:
        return model.model_validate(payload)
    except ValidationError:
        return None
