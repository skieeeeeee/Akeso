"""Test bootstrap.

The environment is switched to `test` before any application module is
imported, so `app.config.settings` resolves the *test* database and no test
can touch development data.
"""

from __future__ import annotations

import os

os.environ["ENVIRONMENT"] = "test"
os.environ.setdefault("JWT_SECRET", "test-secret-value")
os.environ.setdefault("EXPOSE_MOCK_OTP", "true")

from collections.abc import Iterator  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.database import SessionLocal, engine  # noqa: E402
from app.database.metadata import Base  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _schema() -> Iterator[None]:
    """Rebuild the test schema once per run.

    The schema is dropped wholesale rather than via `drop_all`, because
    PostgreSQL native ENUM types outlive their tables and would collide on the
    next run.
    """
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


TABLES = (
    "otp_challenges",
    "red_flags",
    "conversation_answers",
    "conversation_sessions",
    "extracted_medical_data",
    "ayush_assessments",
    "documents",
    "encounters",
    "medical_profiles",
    "consents",
    "accessibility_assessments",
    "patient_preferences",
    "abha_profiles",
    "patients",
)


@pytest.fixture(autouse=True)
def _clean_tables() -> Iterator[None]:
    """Every test starts from an empty database."""
    yield
    with engine.begin() as connection:
        connection.execute(
            text(f"TRUNCATE {', '.join(TABLES)} RESTART IDENTITY CASCADE")
        )


@pytest.fixture
def db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


# --- Journey helpers -------------------------------------------------------


@pytest.fixture
def api() -> str:
    from app.config import settings

    return settings.api_prefix


@pytest.fixture
def sign_in(client: TestClient, api: str):
    """Authenticate a mobile number and return its auth headers + session."""

    def _sign_in(mobile: str = "9812300001", language: str = "en") -> tuple[dict, dict]:
        requested = client.post(
            f"{api}/auth/otp/request", json={"mobile_number": mobile}
        ).json()
        session = client.post(
            f"{api}/auth/otp/verify",
            json={
                "mobile_number": mobile,
                "code": requested["prototype_code"],
                "language": language,
            },
        ).json()
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        return headers, session

    return _sign_in
