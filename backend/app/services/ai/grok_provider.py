"""Grok (x.ai) provider.

The only place an HTTP call to an AI vendor exists. It implements the same
`AiProvider` protocol as `NullProvider`, which means:

* feature code cannot tell which provider it is talking to;
* every expected failure (no key, timeout, rate limit, refusal, malformed
  output) returns `None` rather than raising, so the caller's deterministic
  fallback runs and the patient's session survives.

The API key is read from settings only — it is never sent to the frontend.
"""

from __future__ import annotations

import json
import asyncio
import logging
from typing import Any

import httpx

from app.config import settings

# Worth retrying: rate limits and the transient overload a free tier returns
# under load. A 401 or a 400 will not fix itself, so it is not retried.
_RETRYABLE = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 3
_RETRY_BASE_DELAY = 1.5

log = logging.getLogger("medikiosk.ai.grok")

# x.ai exposes an OpenAI-compatible chat-completions endpoint.
DEFAULT_BASE_URL = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-4"


class GrokProvider:
    name = "grok"

    def __init__(
        self,
        *,
        api_key: str,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self._api_key = api_key
        self._model = model or DEFAULT_MODEL
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout or settings.ai_timeout_seconds

    async def complete_json(
        self,
        *,
        system: str,
        prompt: str,
        max_tokens: int = 2048,
        image_base64: str | None = None,
        image_media_type: str = "image/png",
    ) -> dict[str, Any] | None:
        content: Any = prompt
        if image_base64:
            # Vision request: used only by the OCR fallback provider.
            content = [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_media_type};base64,{image_base64}"},
                },
                {"type": "text", "text": prompt},
            ]

        payload = {
            "model": self._model,
            "max_tokens": max_tokens,
            "temperature": 0,
            # Ask for machine-readable output; we still validate it ourselves.
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": content},
            ],
        }

        response = await self._post_with_retries(payload)
        if response is None:
            return None

        try:
            body = response.json()
            text = body["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            log.warning("grok response was not in the expected shape: %s", exc)
            return None

        return _parse_json_object(text)

    async def _post_with_retries(self, payload: dict[str, Any]) -> httpx.Response | None:
        """POST the request, retrying the failures that are worth retrying.

        Rate limits and "high demand" are transient and common on free tiers —
        two consecutive 503s were enough to make a document fall back to the
        local OCR result, which for handwriting means falling back to garbage.
        A bad key or a bad request is not retried, because it will not fix
        itself.

        @returns the successful response, or None so the caller uses its
                 deterministic fallback.
        """
        delay = _RETRY_BASE_DELAY
        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(
                        f"{self._base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self._api_key}",
                            "Content-Type": "application/json",
                        },
                        json=payload,
                    )
            except httpx.HTTPError as exc:
                log.warning("AI request failed (attempt %s): %s", attempt, exc)
                if attempt == _MAX_ATTEMPTS:
                    return None
            else:
                if response.status_code == 200:
                    return response
                if response.status_code not in _RETRYABLE or attempt == _MAX_ATTEMPTS:
                    log.warning(
                        "AI returned %s: %s",
                        response.status_code,
                        response.text[:200],
                    )
                    return None
                log.info(
                    "AI returned %s, retrying in %.1fs (attempt %s/%s)",
                    response.status_code,
                    delay,
                    attempt,
                    _MAX_ATTEMPTS,
                )
            await asyncio.sleep(delay)
            delay *= 2
        return None


def _parse_json_object(text: str | None) -> dict[str, Any] | None:
    """Pull a JSON object out of the reply, tolerating stray fences."""
    if not text:
        return None
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.lower().startswith("json"):
            candidate = candidate[4:]
    start = candidate.find("{")
    end = candidate.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        parsed = json.loads(candidate[start : end + 1])
    except ValueError:
        return None
    return parsed if isinstance(parsed, dict) else None
