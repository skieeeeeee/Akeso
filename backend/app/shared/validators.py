"""Input normalisation shared by authentication and the personal-info form.

These are pure functions that raise `ValueError` with a patient-readable
message. Pydantic turns that into a 422 whose message the API error handler
surfaces verbatim, so the same rule serves both the schema layer and the
service layer without either depending on the web framework.
"""

from __future__ import annotations

import re
from datetime import date

_NON_DIGITS = re.compile(r"\D")
# Indian mobile numbers: 10 digits beginning 6-9.
_INDIAN_MOBILE = re.compile(r"^[6-9]\d{9}$")


def normalize_mobile(raw: str) -> str:
    """Reduce any common input form to 10 bare digits.

    Accepts "+91 98765 43210", "098765-43210", "9876543210".
    """
    digits = _NON_DIGITS.sub("", raw or "")
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    if not _INDIAN_MOBILE.match(digits):
        raise ValueError("Please enter a valid 10-digit Indian mobile number.")
    return digits


def validate_date_of_birth(value: date) -> date:
    today = date.today()
    if value > today:
        raise ValueError("Date of birth cannot be in the future.")
    if value.year < today.year - 120:
        raise ValueError("Please check the date of birth — that year looks too early.")
    return value


def clean_text(value: str | None, *, max_length: int = 300) -> str | None:
    if value is None:
        return None
    collapsed = re.sub(r"\s+", " ", value).strip()
    return collapsed[:max_length] or None
