"""The migrated schema must match the models.

The rest of the suite builds its schema straight from the SQLAlchemy models,
which is fast but means a migration can drift from the models without any test
noticing. That is exactly what happened with the `language` ENUM: four
languages were added to `Language` and the PostgreSQL type was never altered,
so persisting Marathi, Tamil, Gujarati or Punjabi failed on a real database
while every test passed.

These tests run the real migrations into a scratch database and compare each
native ENUM type against its Python counterpart.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from app.config import settings
from app.shared import enums

# Every native ENUM the migrations create, and the Python enum it mirrors.
ENUM_TYPES: dict[str, type] = {
    "language": enums.Language,
    "gender": enums.Gender,
    "onboarding_status": enums.OnboardingStatus,
    "abha_verification_status": enums.AbhaVerificationStatus,
    "interface_mode": enums.InterfaceMode,
    "font_size": enums.FontSize,
    "contrast_mode": enums.ContrastMode,
    "interaction_preference": enums.InteractionPreference,
    "consent_purpose": enums.ConsentPurpose,
    "consent_status": enums.ConsentStatus,
    "encounter_status": enums.EncounterStatus,
    "encounter_priority": enums.EncounterPriority,
    "document_type": enums.DocumentType,
    "processing_status": enums.ProcessingStatus,
    "red_flag_status": enums.RedFlagStatus,
    "care_system": enums.CareSystem,
}


@pytest.fixture(scope="module")
def migrated_url() -> str:
    """A scratch database with every migration applied, then dropped."""
    base = settings.database_url.rsplit("/", 1)[0]
    name = f"medikiosk_migrations_{uuid.uuid4().hex[:8]}"
    admin = create_engine(f"{base}/postgres", isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(text(f'CREATE DATABASE "{name}"'))
    url = f"{base}/{name}"

    # `alembic/env.py` resolves the URL from settings unless given -x url=...,
    # so pass it that way rather than through sqlalchemy.url.
    config = Config("alembic.ini")
    config.cmd_opts = SimpleNamespace(x=[f"url={url}"])
    try:
        command.upgrade(config, "head")
        yield url
    finally:
        with admin.connect() as connection:
            # Terminate anything still attached, or the drop blocks.
            connection.execute(
                text(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = :name AND pid <> pg_backend_pid()"
                ),
                {"name": name},
            )
            connection.execute(text(f'DROP DATABASE IF EXISTS "{name}"'))
        admin.dispose()


def _labels(url: str, type_name: str) -> set[str]:
    engine = create_engine(url)
    try:
        with engine.connect() as connection:
            rows = connection.execute(
                text(
                    "SELECT e.enumlabel FROM pg_type t "
                    "JOIN pg_enum e ON e.enumtypid = t.oid "
                    "WHERE t.typname = :name"
                ),
                {"name": type_name},
            ).scalars()
            return set(rows)
    finally:
        engine.dispose()


class TestNativeEnumsMatchTheModels:
    @pytest.mark.parametrize("type_name", sorted(ENUM_TYPES))
    def test_the_database_type_has_every_python_value(
        self, migrated_url: str, type_name: str
    ):
        expected = {member.value for member in ENUM_TYPES[type_name]}
        actual = _labels(migrated_url, type_name)
        assert actual, f"ENUM type {type_name!r} does not exist after migration"
        missing = expected - actual
        assert missing == set(), (
            f"{type_name}: the model allows {sorted(missing)} but the database "
            "type does not. Add a migration with ALTER TYPE ... ADD VALUE."
        )

    def test_every_interface_language_is_storable(self, migrated_url: str):
        """The one that bit us, stated plainly."""
        assert _labels(migrated_url, "language") >= {
            language.value for language in enums.Language
        }


class TestManagedDatabaseUrls:
    """Managed hosts hand out `postgres://…`; SQLAlchemy needs a driver.

    Render, Railway and Heroku all inject the bare scheme. Without rewriting
    it, a deploy fails at first connection with an unhelpful parse error, or
    reaches for psycopg2, which this project does not install.
    """

    @pytest.mark.parametrize(
        "given,expected",
        [
            (
                "postgres://u:p@host:5432/db",
                "postgresql+psycopg://u:p@host:5432/db",
            ),
            (
                "postgresql://u:p@host:5432/db",
                "postgresql+psycopg://u:p@host:5432/db",
            ),
            # Already explicit: left exactly as given.
            (
                "postgresql+psycopg://u:p@host:5432/db",
                "postgresql+psycopg://u:p@host:5432/db",
            ),
        ],
    )
    def test_the_driver_is_added_when_missing(self, given: str, expected: str):
        from app.config.settings import Settings

        assert Settings(database_url=given).database_url == expected
        assert Settings(test_database_url=given).test_database_url == expected
