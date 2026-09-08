"""The provenance-carrying clinical value used across every medical section.

One shape for every clinical fact means the onboarding form, Phase 2's OCR
extraction and a future clinician edit all write the same thing, and the UI
can always say where a value came from and whether it was verified.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.shared.enums import ClinicalSource


class ClinicalItem(BaseModel):
    """A single medical fact, e.g. one allergy or one medication."""

    model_config = ConfigDict(extra="forbid")

    value: str = Field(min_length=1, max_length=300)
    # Free-form structured extras, e.g. {"dose": "500 mg", "frequency": "BD"}.
    attributes: dict[str, str] = Field(default_factory=dict)
    source: ClinicalSource = ClinicalSource.PATIENT
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    verified: bool = False
    # Set when source is DOCUMENT, so the UI can link back to the scan.
    document_id: str | None = None
    note: str | None = Field(default=None, max_length=500)
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def to_json(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def parse_items(raw: list[dict[str, Any]] | None) -> list[ClinicalItem]:
    """Read stored JSONB into typed items, skipping anything unparseable.

    A single malformed row must not make a patient's whole profile unreadable.
    """
    items: list[ClinicalItem] = []
    for entry in raw or []:
        try:
            items.append(ClinicalItem.model_validate(entry))
        except Exception:  # noqa: BLE001 - defensive: skip corrupt rows only
            continue
    return items


def dump_items(items: list[ClinicalItem]) -> list[dict[str, Any]]:
    return [item.to_json() for item in items]
