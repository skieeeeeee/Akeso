"""Add the four regional languages to the language enum.

Marathi, Tamil, Gujarati and Punjabi were added to `app.shared.enums.Language`
when localisation was built, but the PostgreSQL ENUM type was never altered to
match. The tests build their schema from the models, so the type had all six
values there and the gap was invisible — while on a migrated database any
attempt to persist one of the four failed with a database error, surfaced to
the patient as a 503 and a silently reverted language.

`ALTER TYPE ... ADD VALUE` is supported inside a transaction from PostgreSQL 12
onwards, provided the new value is not used in the same transaction.

Revision ID: d4a1c7e93b28
Revises: c32f70b87536
"""

from __future__ import annotations

from alembic import op

revision = "d4a1c7e93b28"
down_revision = "c32f70b87536"
branch_labels = None
depends_on = None

# Order matters only for `enumsortorder`; it has no behavioural effect.
NEW_LANGUAGES = ("mr", "ta", "gu", "pa")


def upgrade() -> None:
    for code in NEW_LANGUAGES:
        op.execute(f"ALTER TYPE language ADD VALUE IF NOT EXISTS '{code}'")


def downgrade() -> None:
    """No-op.

    PostgreSQL cannot remove a value from an ENUM type. Rebuilding the type
    would mean rewriting every column that uses it, and would fail outright if
    any row already held one of these languages — which is worse than leaving
    four unused labels in place. Same convention as the other enums here.
    """
