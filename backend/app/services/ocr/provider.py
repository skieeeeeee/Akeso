"""OCR boundary.

Everything downstream sees only `OcrResult`. Nothing in the document pipeline,
the interview engine or the UI knows which engine produced the text, so the
engine can be swapped without touching feature code.

Providers are tried in order and each one returns `None` when it simply cannot
handle the input (wrong media type, engine not installed). A raised exception
is caught, recorded and treated as "this provider failed" — never as a request
failure, because the document itself must survive regardless.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.config import settings

log = logging.getLogger("medikiosk.ocr")

IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}
TEXT_TYPES = {"text/plain", "text/csv"}


@dataclass(frozen=True, slots=True)
class OcrResult:
    text: str
    engine: str
    # Mean per-line confidence where the engine reports it, else a nominal value.
    confidence: float


class OcrProvider(Protocol):
    name: str

    def read(self, path: Path, mime_type: str) -> OcrResult | None: ...


class PlaintextProvider:
    """Already-digital records (.txt/.csv). Also what the demo fixtures use."""

    name = "plaintext"

    def read(self, path: Path, mime_type: str) -> OcrResult | None:
        if mime_type not in TEXT_TYPES:
            return None
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        return OcrResult(text=text, engine=self.name, confidence=1.0) if text else None


class LocalOcrProvider:
    """PaddleOCR models running locally through ONNX Runtime.

    Imported lazily so a missing or broken install degrades this provider to
    unavailable instead of preventing the application from starting.
    """

    name = "rapidocr"

    def read(self, path: Path, mime_type: str) -> OcrResult | None:
        if mime_type not in IMAGE_TYPES:
            return None
        try:
            from rapidocr_onnxruntime import RapidOCR
        except ImportError:
            log.info("local OCR engine is not installed; skipping")
            return None

        engine = _local_engine(RapidOCR)
        result, _ = engine(_prepared(path))
        if not result:
            return None

        lines = [str(line[1]).strip() for line in result if len(line) > 1 and line[1]]
        scores = [float(line[2]) for line in result if len(line) > 2 and line[2] is not None]
        text = "\n".join(line for line in lines if line)
        if not text:
            return None
        return OcrResult(
            text=text,
            engine=self.name,
            confidence=round(sum(scores) / len(scores), 3) if scores else 0.5,
        )


# Below this width the recognition models see too few pixels per character on
# a phone photo. Upscaling costs ~0.2s and measurably improves printed text;
# it does not rescue handwriting, which these models are not trained for.
_MIN_WIDTH = 1600


def _prepared(path: Path):
    """The image, upscaled if it is small. Falls back to the path on any error.

    Deliberately conservative: no deskew, binarisation or denoising. Those
    helped nothing on the prescriptions tested here and each one can destroy
    faint strokes, so the original pixels are what the engine sees apart from
    a clean Lanczos resize.
    """
    try:
        import numpy as np
        from PIL import Image

        with Image.open(path) as image:
            image = image.convert("RGB")
            width, height = image.size
            if width >= _MIN_WIDTH:
                return str(path)
            scale = min(_MIN_WIDTH / width, 3.0)
            resized = image.resize(
                (int(width * scale), int(height * scale)), Image.LANCZOS
            )
            return np.array(resized)
    except Exception as exc:  # noqa: BLE001 - never fail a read over a resize
        log.info("could not pre-scale %s (%s); using the original", path.name, exc)
        return str(path)


_ENGINE_CACHE: dict[str, object] = {}


def _local_engine(factory: type) -> object:
    """One engine instance per process — construction loads the models."""
    engine = _ENGINE_CACHE.get("local")
    if engine is None:
        engine = factory()
        _ENGINE_CACHE["local"] = engine
    return engine


class AiVisionProvider:
    """Transcription by the configured AI provider, for hard scans.

    Only reachable when an AI provider is actually configured; otherwise it
    reports unavailable like any other provider.
    """

    name = "ai_vision"

    async def read_async(self, path: Path, mime_type: str) -> OcrResult | None:
        if mime_type not in IMAGE_TYPES:
            return None
        from app.services.ai import get_provider

        provider = get_provider()
        if provider.name == "none":
            return None

        import base64

        payload = base64.b64encode(path.read_bytes()).decode()
        result = await provider.complete_json(
            system=(
                "You transcribe scanned medical documents. Reproduce the text "
                "exactly as printed, preserving line breaks and numbers. Do "
                "not interpret, correct, summarise or add anything."
            ),
            prompt='Transcribe every line. Return {"text": "..."}',
            image_base64=payload,
            image_media_type=mime_type,
        )
        text = (result or {}).get("text")
        if not isinstance(text, str) or not text.strip():
            return None
        return OcrResult(text=text.strip(), engine=self.name, confidence=0.85)

    def read(self, path: Path, mime_type: str) -> OcrResult | None:  # pragma: no cover
        raise NotImplementedError("use read_async")


# Below this, the local engine is guessing rather than reading.
_LOW_CONFIDENCE = 0.85
# A document with almost no ordinary words in it is not a document we read.
_MIN_WORDLIKE_RATIO = 0.5


def _looks_unreliable(result: OcrResult) -> bool:
    """Whether a local read is poor enough to be worth a second opinion.

    Two signals, both cheap. Neither is clever: the point is only to stop a
    confidently-wrong page of glyphs from being treated as a successful read.
    """
    if result.confidence < _LOW_CONFIDENCE:
        return True
    tokens = re.findall(r"[A-Za-z]{2,}", result.text)
    if not tokens:
        return True
    # Real words are mostly lower case with at most one capital. Strings like
    # "Hfaspos" or "xoclsfT" fail this; "Paracetamol" and "mg" pass.
    wordlike = sum(1 for token in tokens if token[1:].islower())
    return wordlike / len(tokens) < _MIN_WORDLIKE_RATIO


class OcrUnavailable(RuntimeError):
    """No provider could produce text. The document is still stored."""


async def run_ocr(path: Path, mime_type: str) -> OcrResult:
    """Read a document with the first provider that can.

    @raises OcrUnavailable when every provider declined or failed.
    """
    mode = (settings.ocr_provider or "auto").lower()
    if mode == "off":
        raise OcrUnavailable("Reading documents is switched off on this server.")

    reasons: list[str] = []

    # Plain text first: exact, free, and no engine can beat it.
    try:
        result = PlaintextProvider().read(path, mime_type)
        if result:
            log.info("read %s via %s", path.name, result.engine)
            return result
    except Exception as exc:  # noqa: BLE001 - one engine failing is not fatal
        reasons.append(f"plaintext: {exc}")

    local: OcrResult | None = None
    if mode in ("auto", "local"):
        try:
            local = LocalOcrProvider().read(path, mime_type)
        except Exception as exc:  # noqa: BLE001
            reasons.append(f"rapidocr: {exc}")
            log.warning("OCR provider rapidocr failed: %s", exc)

    # Escalate to a vision model when the local engine produced nothing, or
    # produced something that does not read like a document.
    #
    # This used to return the local result the moment it was non-empty, which
    # meant a page of garbage counted as success and the vision model was
    # never asked. Handwriting is exactly where that mattered: the local
    # models are trained on print, and a vision model does far better because
    # it reads a prescription in context rather than glyph by glyph.
    if mode in ("auto", "ai") and (local is None or _looks_unreliable(local)):
        try:
            better = await AiVisionProvider().read_async(path, mime_type)
        except Exception as exc:  # noqa: BLE001
            reasons.append(f"ai_vision: {exc}")
            log.warning("AI vision OCR failed: %s", exc)
        else:
            if better:
                log.info(
                    "read %s via %s (%.2f), escalated from %s",
                    path.name,
                    better.engine,
                    better.confidence,
                    local.engine if local else "nothing",
                )
                return better

    if local:
        log.info("read %s via %s (%.2f)", path.name, local.engine, local.confidence)
        return local

    raise OcrUnavailable(
        "We could not read any text from this file. "
        + (f"({reasons[-1]})" if reasons else "The image may be too blurred.")
    )
