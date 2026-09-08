"""Reusable column types."""

from __future__ import annotations

from enum import Enum
from typing import Any

import sqlalchemy as sa


def enum_column(py_enum: type[Enum], name: str) -> sa.Enum:
    """A PostgreSQL ENUM that stores the enum *value*, not the member name.

    Without ``values_callable`` SQLAlchemy persists "MALE" instead of "male",
    which would not match the API contract or the frontend union types.
    """
    return sa.Enum(
        py_enum,
        name=name,
        values_callable=lambda enum_cls: [member.value for member in enum_cls],
        native_enum=True,
        create_constraint=False,
    )


def json_list_default() -> list[Any]:
    return []


def json_dict_default() -> dict[str, Any]:
    return {}
