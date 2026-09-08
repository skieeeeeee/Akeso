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
