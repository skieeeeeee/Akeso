"""Base Pydantic configuration shared by every API schema."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class ApiModel(BaseModel):
    """Response/request base.

    `from_attributes` lets schemas read directly off SQLAlchemy models, which
    keeps the mapping layer thin and avoids hand-written converters.

    `use_enum_values` is deliberately NOT set: parsed enum fields stay as enum
    members so service and rule-engine code can rely on them. JSON responses
    still serialise to the enum's string value.
    """

    model_config = ConfigDict(from_attributes=True)


class UtcModel(ApiModel):
    """Base for responses whose timestamps must be byte-stable.

    PostgreSQL returns `timestamptz` in the session timezone, while a
    just-assigned value is UTC. Normalising on the way out means an
    idempotent endpoint returns the identical string on a repeat call.
    """

    @field_serializer("*", when_used="unless-none")
    def _utc_timestamps(self, value: object) -> object:
        if isinstance(value, datetime) and value.tzinfo is not None:
            return value.astimezone(UTC)
        return value


class Message(ApiModel):
    message: str
