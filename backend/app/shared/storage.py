"""Local file storage for patient-uploaded records.

Files are written before any processing is attempted, so a later OCR failure
(Phase 2) can never lose the patient's document.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

from app.config import settings
from app.shared.errors import ValidationFailedError

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]")

ALLOWED_MIME_TYPES: dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "application/pdf": ".pdf",
    # Already-digital records. The OCR layer reads these directly, which is
    # also what makes the demo documents reproducible without an OCR engine.
    "text/plain": ".txt",
    "text/csv": ".csv",
}


def safe_name(file_name: str) -> str:
    cleaned = _UNSAFE.sub("_", Path(file_name).name).strip("._")
    return cleaned[-120:] or "upload"


def validate_upload(mime_type: str, size_bytes: int) -> None:
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValidationFailedError(
            "Please upload a photo (PNG or JPEG), a PDF, or a text copy of your record.",
            details={"field": "file", "received": mime_type},
        )
    if size_bytes <= 0:
        raise ValidationFailedError("That file appears to be empty.", details={"field": "file"})
    if size_bytes > settings.max_upload_bytes:
        limit_mb = settings.max_upload_bytes // (1024 * 1024)
        raise ValidationFailedError(
            f"That file is larger than {limit_mb} MB. Please upload a smaller photo.",
            details={"field": "file"},
        )


def save(patient_id: uuid.UUID, file_name: str, content: bytes) -> str:
    """Write the file and return its path relative to the upload directory."""
    directory = settings.upload_dir / str(patient_id)
    directory.mkdir(parents=True, exist_ok=True)
    unique = f"{uuid.uuid4().hex[:12]}_{safe_name(file_name)}"
    (directory / unique).write_bytes(content)
    return f"{patient_id}/{unique}"


def absolute_path(relative_path: str) -> Path:
    return settings.upload_dir / relative_path


def delete(relative_path: str) -> None:
    absolute_path(relative_path).unlink(missing_ok=True)
