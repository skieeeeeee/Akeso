"""Mock ABHA verification.

THIS IS NOT ABDM. No network call is made and no government service is
contacted. Verification is a local format check with a deterministic outcome,
which keeps the demo predictable and makes the failure path reproducible.

The function signature is the seam a real ABDM client would replace.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Real ABHA numbers are 14 digits, usually shown as 12-3456-7890-1234.
_ABHA_NUMBER = re.compile(r"^\d{14}$")
# ABHA addresses look like an identifier followed by a domain.
_ABHA_ADDRESS = re.compile(r"^[a-z0-9][a-z0-9._-]{2,30}@[a-z]{3,10}$", re.IGNORECASE)

# Reserved identifiers that deliberately exercise the failure paths so the
# graceful-fallback UI can be demonstrated on demand.
UNAVAILABLE_SENTINEL = "00000000000000"
REJECTED_SENTINEL = "99999999999999"


@dataclass(frozen=True, slots=True)
class MockVerification:
    verified: bool
    normalized_id: str
    reason: str | None = None


class RegistryUnavailable(RuntimeError):
    """The (mock) registry could not be reached."""


def normalize_abha_id(raw: str) -> str:
    """Strip separators from a number; lower-case an address."""
    candidate = (raw or "").strip()
    if "@" in candidate:
        return candidate.lower()
    return re.sub(r"[\s-]", "", candidate)


def format_abha_number(digits: str) -> str:
    """Present 14 digits as 12-3456-7890-1234."""
    if not _ABHA_NUMBER.match(digits):
        return digits
    return f"{digits[:2]}-{digits[2:6]}-{digits[6:10]}-{digits[10:]}"


def verify(raw: str) -> MockVerification:
    """Check an ABHA identifier.

    @raises RegistryUnavailable to simulate the registry being down, so the
            caller's fallback path can be exercised.
    """
    normalized = normalize_abha_id(raw)

    if normalized == UNAVAILABLE_SENTINEL:
        raise RegistryUnavailable("Mock registry is unavailable")

    if normalized == REJECTED_SENTINEL:
        return MockVerification(
            verified=False,
            normalized_id=format_abha_number(normalized),
            reason="This health ID could not be verified.",
        )

    if _ABHA_NUMBER.match(normalized):
        return MockVerification(verified=True, normalized_id=format_abha_number(normalized))

    if _ABHA_ADDRESS.match(normalized):
        return MockVerification(verified=True, normalized_id=normalized)

    return MockVerification(
        verified=False,
        normalized_id=normalized,
        reason="Enter a 14-digit ABHA number or an ABHA address like name@abdm.",
    )
