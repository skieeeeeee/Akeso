"""Reading text aloud.

The point of the server-side path: a phone or kiosk commonly has no installed
voice for Marathi, Gujarati or Punjabi, so the browser cannot speak in those
languages at all. These tests pin the two properties that matter — the key
never reaches the client, and a failure always degrades to the browser rather
than breaking a page.
"""

from __future__ import annotations

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.services import speech


class TestStatus:
    def test_it_reports_off_when_no_key_is_configured(
        self, client: TestClient, api: str, monkeypatch
    ):
        monkeypatch.setattr(settings, "elevenlabs_api_key", None)
        body = client.get(f"{api}/speech/status").json()
        assert body["available"] is False

    def test_it_reports_on_when_configured(
        self, client: TestClient, api: str, monkeypatch
    ):
        monkeypatch.setattr(settings, "elevenlabs_api_key", "k")
        assert client.get(f"{api}/speech/status").json()["available"] is True

    def test_the_key_is_never_sent_to_the_client(
        self, client: TestClient, api: str, monkeypatch
    ):
        """The whole reason this is a server endpoint."""
        monkeypatch.setattr(settings, "elevenlabs_api_key", "super-secret-key")
        assert "super-secret-key" not in client.get(f"{api}/speech/status").text
        schema = client.get("/openapi.json").text
        assert "super-secret-key" not in schema
        assert "elevenlabs_api_key" not in schema


class TestSynthesis:
    async def test_it_returns_audio(self, monkeypatch):
        monkeypatch.setattr(settings, "elevenlabs_api_key", "k")

        async def post(self, url, **kwargs):  # noqa: ANN001
            assert kwargs["headers"]["xi-api-key"] == "k"
            return httpx.Response(200, content=b"ID3-audio-bytes")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        assert await speech.synthesise("Hello", "en") == b"ID3-audio-bytes"

    async def test_it_declines_when_not_configured(self, monkeypatch):
        monkeypatch.setattr(settings, "elevenlabs_api_key", None)
        with pytest.raises(speech.SpeechUnavailable):
            await speech.synthesise("Hello", "en")

    async def test_an_upstream_failure_is_not_an_error_for_the_caller(
        self, monkeypatch
    ):
        """A scoped-out key, an exhausted quota and a blip look the same."""
        monkeypatch.setattr(settings, "elevenlabs_api_key", "k")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(401, text="missing the permission text_to_speech")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        with pytest.raises(speech.SpeechUnavailable):
            await speech.synthesise("Hello", "en")

    async def test_long_text_is_truncated_rather_than_refused(self, monkeypatch):
        """A quota is spent per character, so a whole page is not sent."""
        monkeypatch.setattr(settings, "elevenlabs_api_key", "k")
        sent: dict = {}

        async def post(self, url, **kwargs):  # noqa: ANN001
            sent.update(kwargs["json"])
            return httpx.Response(200, content=b"audio")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        await speech.synthesise("word " * 500, "hi")
        assert len(sent["text"]) <= speech.MAX_CHARACTERS


class TestEndpoint:
    def test_it_requires_a_signed_in_patient(self, client: TestClient, api: str):
        """Speaking spends a character quota, so it is not left open."""
        response = client.post(f"{api}/speech", json={"text": "hello"})
        assert response.status_code == 401

    def test_it_returns_mp3_for_a_signed_in_patient(
        self, client: TestClient, api: str, sign_in, monkeypatch
    ):
        headers, _ = sign_in("9812450001")
        monkeypatch.setattr(settings, "elevenlabs_api_key", "k")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(200, content=b"ID3-audio")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        response = client.post(
            f"{api}/speech",
            json={"text": "आज आपको क्या तकलीफ़ है?", "language": "hi"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "audio/mpeg"
        assert response.content == b"ID3-audio"

    def test_it_answers_503_so_the_client_can_fall_back(
        self, client: TestClient, api: str, sign_in, monkeypatch
    ):
        headers, _ = sign_in("9812450002")
        monkeypatch.setattr(settings, "elevenlabs_api_key", None)
        response = client.post(
            f"{api}/speech", json={"text": "hello"}, headers=headers
        )
        assert response.status_code == 503
        # A patient-safe message, not an upstream error dump.
        assert "message" in response.json()["error"]


class TestTheSpeechProbeSaysWhy:
    """`/status` reporting available is not evidence that speech works.

    It stayed true on a deployment where every request failed, because the
    configured voice was a shared library voice the free plan may not use.
    From outside, that 402 is indistinguishable from a bad key or an
    exhausted quota, and the patient just silently gets the browser voice.
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status,reason",
        [
            (401, "bad_key_or_missing_permission"),
            (402, "paid_plan_required"),
            (404, "voice_not_found"),
            (429, "quota_or_rate_limit"),
            (500, "upstream_error"),
        ],
    )
    async def test_it_names_the_upstream_failure(self, monkeypatch, status, reason):
        import httpx

        from app.services import speech

        monkeypatch.setattr(speech.provider.settings, "elevenlabs_api_key", "secret-key")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(status, text="upstream said no")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await speech.probe()
        assert result["ok"] is False
        assert result["reason"] == reason
        assert result["http_status"] == status

    @pytest.mark.asyncio
    async def test_it_reports_success_with_the_audio_size(self, monkeypatch):
        import httpx

        from app.services import speech

        monkeypatch.setattr(speech.provider.settings, "elevenlabs_api_key", "secret-key")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(200, content=b"ID3" + b"\x00" * 500)

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await speech.probe()
        assert result["ok"] is True
        assert result["reason"] is None
        assert "503 bytes" in str(result["detail"])

    @pytest.mark.asyncio
    async def test_it_says_so_when_no_key_is_set(self, monkeypatch):
        from app.services import speech

        monkeypatch.setattr(speech.provider.settings, "elevenlabs_api_key", None)
        result = await speech.probe()
        assert result["ok"] is False
        assert result["reason"] == "not_configured"
        assert result["key_present"] is False

    @pytest.mark.asyncio
    async def test_it_never_returns_the_api_key(self, monkeypatch):
        import httpx

        from app.services import speech

        monkeypatch.setattr(speech.provider.settings, "elevenlabs_api_key", "secret-key")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(401, text="missing permission")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        result = await speech.probe()
        assert "secret-key" not in repr(result)

    @pytest.mark.asyncio
    async def test_the_patient_facing_message_stays_plain(self, monkeypatch):
        """The upstream body must not reach the text a client displays."""
        import httpx

        from app.services import speech

        monkeypatch.setattr(speech.provider.settings, "elevenlabs_api_key", "k")

        async def post(self, url, **kwargs):  # noqa: ANN001
            return httpx.Response(402, text='{"detail":{"status":"paid_plan_required"}}')

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        with pytest.raises(speech.SpeechUnavailable) as caught:
            await speech.synthesise("hello", "en")
        assert "paid_plan_required" not in str(caught.value)
        assert "paid_plan_required" in caught.value.technical


class TestAConcurrencyRejectionIsRetried:
    """A free ElevenLabs plan allows four concurrent requests.

    A patient moving quickly through questions hits 429 with nothing wrong,
    and every rejection used to fall straight through to a browser voice that
    does not exist for Marathi, Gujarati or Punjabi — so they pressed listen
    and heard silence. The AI provider has retried these from the start.
    """

    def _fast(self, monkeypatch):
        from app.services.speech import provider

        monkeypatch.setattr(provider, "_RETRY_BASE_DELAY", 0.0)
        monkeypatch.setattr(provider.settings, "elevenlabs_api_key", "k")

    @pytest.mark.asyncio
    async def test_a_429_then_success(self, monkeypatch):
        import httpx

        from app.services import speech

        self._fast(monkeypatch)
        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            if len(calls) < 3:
                return httpx.Response(429, text="too many concurrent requests")
            return httpx.Response(200, content=b"ID3" + b"\x00" * 100)

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        audio = await speech.synthesise("hello", "mr")
        assert audio.startswith(b"ID3")
        assert len(calls) == 3, "should have retried twice before succeeding"

    @pytest.mark.asyncio
    async def test_a_bad_key_is_not_retried(self, monkeypatch):
        """It will not fix itself, and retrying only delays the fallback."""
        import httpx

        from app.services import speech

        self._fast(monkeypatch)
        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            return httpx.Response(401, text="invalid api key")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        with pytest.raises(speech.SpeechUnavailable) as caught:
            await speech.synthesise("hello", "en")
        assert caught.value.reason == "bad_key_or_missing_permission"
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_it_gives_up_after_three_attempts(self, monkeypatch):
        import httpx

        from app.services import speech

        self._fast(monkeypatch)
        calls = []

        async def post(self, url, **kwargs):  # noqa: ANN001
            calls.append(url)
            return httpx.Response(429, text="rate limited")

        monkeypatch.setattr(httpx.AsyncClient, "post", post)
        with pytest.raises(speech.SpeechUnavailable) as caught:
            await speech.synthesise("hello", "gu")
        assert caught.value.reason == "quota_or_rate_limit"
        assert len(calls) == 3
