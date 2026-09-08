"""AI schema validation and fallback.

The contract these tests defend: a model can only ever contribute
schema-valid data, and any failure looks exactly like AI being switched off.
"""

from __future__ import annotations

import pytest

from app.services.ai import NullProvider, get_provider, provider_status, structured
from app.services.ai.grok_provider import GrokProvider, _parse_json_object
from app.services.ai.schemas import (
    AnswerUnderstanding,
    DocumentExtraction,
    FollowUpSuggestions,
    HistorySummary,
)


class TestStructuredValidation:
    def test_none_stays_none(self):
        assert structured(AnswerUnderstanding, None) is None

    def test_a_valid_payload_parses(self):
        parsed = structured(
            AnswerUnderstanding,
            {"facts": [{"value": "Diabetes", "section": "past_medical_history"}]},
        )
        assert parsed is not None
        assert parsed.facts[0].value == "Diabetes"
        assert parsed.is_negative is False

    def test_an_unknown_key_is_rejected_not_absorbed(self):
        # extra="forbid": a model improvising fields means we do not trust it.
        assert structured(
            AnswerUnderstanding, {"facts": [], "diagnosis": "diabetes mellitus"}
        ) is None

    def test_a_wrong_type_is_rejected(self):
        assert structured(AnswerUnderstanding, {"facts": "diabetes"}) is None

    def test_confidence_outside_range_is_rejected(self):
        assert structured(
            AnswerUnderstanding,
            {"facts": [{"value": "x", "section": "allergies", "confidence": 4.2}]},
        ) is None

    def test_an_unknown_entity_type_is_rejected(self):
        assert structured(
            DocumentExtraction,
            {"entities": [{"entity_type": "prognosis", "value": "poor"}]},
        ) is None

    def test_a_valid_document_extraction_parses(self):
        parsed = structured(
            DocumentExtraction,
            {
                "document_date": "2026-03-10",
                "entities": [
                    {
                        "entity_type": "investigation",
                        "value": "Haemoglobin",
                        "numeric_value": "10.2",
                        "unit": "g/dL",
                        "reference_range": "13.0-17.0",
                    }
                ],
            },
        )
        assert parsed is not None
        assert parsed.entities[0].value == "Haemoglobin"

    def test_a_flood_of_entities_is_capped(self):
        assert structured(
            DocumentExtraction,
            {"entities": [{"entity_type": "note", "value": f"n{i}"} for i in range(200)]},
        ) is None

    def test_follow_ups_are_capped_at_three(self):
        payload = {
            "questions": [
                {"text_en": f"Question number {i}?", "text_hi": "प्रश्न", "section": "allergies"}
                for i in range(5)
            ]
        }
        assert structured(FollowUpSuggestions, payload) is None

    def test_a_too_short_summary_is_rejected(self):
        assert structured(HistorySummary, {"summary_en": "ok"}) is None


class TestNullProvider:
    @pytest.mark.asyncio
    async def test_it_returns_none_rather_than_raising(self):
        provider = NullProvider()
        assert await provider.complete_json(system="s", prompt="p") is None

    def test_it_is_the_default(self):
        assert get_provider().name == "none"
        assert provider_status() == {
            "provider": "none",
            "available": False,
            "detail": None,
        }


class TestGrokParsing:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ('{"a": 1}', {"a": 1}),
            ('```json\n{"a": 1}\n```', {"a": 1}),
            ('Here you go: {"a": 1} hope that helps', {"a": 1}),
        ],
    )
    def test_it_recovers_json_from_a_chatty_reply(self, raw, expected):
        assert _parse_json_object(raw) == expected

    @pytest.mark.parametrize("raw", ["", None, "no json here", "[1,2,3]", "{broken"])
    def test_it_refuses_anything_it_cannot_parse(self, raw):
        assert _parse_json_object(raw) is None

    @pytest.mark.asyncio
    async def test_a_network_failure_returns_none(self, monkeypatch):
        import httpx

        provider = GrokProvider(api_key="test-key")

        class Failing:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def post(self, *args, **kwargs):
                raise httpx.ConnectError("unreachable")

        monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: Failing())
        assert await provider.complete_json(system="s", prompt="p") is None

    @pytest.mark.asyncio
    async def test_a_rate_limit_returns_none(self, monkeypatch):
        import httpx

        provider = GrokProvider(api_key="test-key")

        class RateLimited:
            status_code = 429
            text = "slow down"

            def json(self):
                return {}

        class Client:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def post(self, *args, **kwargs):
                return RateLimited()

        monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: Client())
        assert await provider.complete_json(system="s", prompt="p") is None


class TestTransientFailuresAreRetried:
    """Free tiers return 503 under load, and it clears in a second.

    Two consecutive 503s were enough to make a handwritten prescription fall
    back to the local OCR result — which for handwriting means falling back to
    garbage. A transient failure is retried; a permanent one is not, because
    it will not fix itself.
    """

    def _provider(self, monkeypatch):
        from app.services.ai import grok_provider

        monkeypatch.setattr(grok_provider, "_RETRY_BASE_DELAY", 0.0)
        return grok_provider.GrokProvider(
            api_key="k", model="m", base_url="https://example.invalid/v1", timeout=5
        )

    async def test_a_503_then_success(self, monkeypatch):
        import httpx

        from app.services.ai import grok_provider

        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            if len(calls) < 3:
                return httpx.Response(503, text="high demand")
            return httpx.Response(
                200,
                json={"choices": [{"message": {"content": '{"text": "read"}'}}]},
            )

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await self._provider(monkeypatch).complete_json(
            system="s", prompt="p"
        )
        assert result == {"text": "read"}
        assert len(calls) == 3, "should have retried twice before succeeding"

    async def test_a_bad_key_is_not_retried(self, monkeypatch):
        import httpx

        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            return httpx.Response(401, text="invalid api key")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await self._provider(monkeypatch).complete_json(
            system="s", prompt="p"
        )
        assert result is None
        assert len(calls) == 1, "a permanent failure must not be retried"

    async def test_it_gives_up_and_lets_the_caller_fall_back(self, monkeypatch):
        import httpx

        from app.services.ai import grok_provider

        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            return httpx.Response(503, text="high demand")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await self._provider(monkeypatch).complete_json(
            system="s", prompt="p"
        )
        assert result is None
        assert len(calls) == grok_provider._MAX_ATTEMPTS
