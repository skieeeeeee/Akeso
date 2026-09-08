"""Application configuration.

Every externally-controlled value enters the application here and nowhere
else, so behaviour differences between dev, test and a future deployment are
visible in one file.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env", BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application -------------------------------------------------------
    app_name: str = "MediKiosk"
    environment: str = Field(default="development")
    api_prefix: str = "/api/v1"
    debug: bool = True

    # --- Database ----------------------------------------------------------
    database_url: str = Field(
        default="postgresql+psycopg://localhost:5432/medikiosk",
        description="SQLAlchemy URL for PostgreSQL.",
    )
    test_database_url: str = Field(
        default="postgresql+psycopg://localhost:5432/medikiosk_test",
    )
    sql_echo: bool = False

    @field_validator("database_url", "test_database_url", mode="after")
    @classmethod
    def _use_the_psycopg_driver(cls, value: str) -> str:
        """Accept the URL shape managed hosts actually hand out.

        Render, Railway, Heroku and friends inject `postgres://…`. SQLAlchemy
        needs a driver, and this project pins psycopg 3, so both of the bare
        forms are rewritten rather than failing at connect time with an
        unhelpful "could not parse" or silently reaching for psycopg2.
        """
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return "postgresql+psycopg://" + value[len(prefix) :]
        return value

    # --- Auth --------------------------------------------------------------
    jwt_secret: str = Field(default="dev-only-change-me", min_length=8)
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 12 * 60

    # --- Mock OTP (prototype) ---------------------------------------------
    otp_ttl_seconds: int = 300
    otp_max_attempts: int = 5
    # When true the generated OTP is returned by the request endpoint so the
    # prototype can be demonstrated without an SMS gateway. The UI shows it
    # inside an explicit "prototype mode" notice — never disguised as a real
    # delivery. MUST be false anywhere real patients exist.
    expose_mock_otp: bool = True
    # A single code accepted for every mobile number, so the prototype can be
    # demonstrated without an SMS gateway and without reading the code off the
    # screen each time.
    #
    # This removes the only thing standing between a phone number and that
    # patient's record. It is no weaker than `expose_mock_otp`, which already
    # hands the real code to the caller — but it is permanent rather than
    # per-request, so it must be empty anywhere real patients could sign in.
    # Set to "" to restore random six-digit codes.
    dev_fixed_otp: str = "12345"

    # --- ABHA (mocked) -----------------------------------------------------
    # No ABDM network call exists in this codebase. This flag documents that
    # and keeps the contract ready for a real integration later.
    abha_mock_mode: bool = True

    # --- AI provider (Phase 2) --------------------------------------------
    ai_provider: str = Field(default="none", description="none | grok")
    ai_api_key: str | None = None
    ai_model: str | None = None
    ai_base_url: str | None = None
    ai_timeout_seconds: float = 20.0

    # --- Speech (text to speech) -------------------------------------------
    # ElevenLabs reads questions aloud for the languages a device has no voice
    # for. Marathi, Gujarati and Punjabi commonly have none installed, which
    # is the gap this closes.
    #
    # The key stays server-side: the browser calls our own endpoint, which
    # proxies to ElevenLabs. A Vite build inlines anything it can see, so a
    # key given to the client would be readable by every visitor.
    #
    # Unset means the browser's own speech synthesis is used, exactly as
    # before — this is an upgrade, never a dependency.
    elevenlabs_api_key: str | None = None
    elevenlabs_model: str = "eleven_turbo_v2_5"
    # A multilingual voice a free ElevenLabs plan can actually use. Several
    # of the widely quoted ids are shared "library" voices and answer 402
    # paid_plan_required on a free key; this one does not. Verified to return
    # audio for all six supported languages.
    elevenlabs_voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    elevenlabs_timeout_seconds: float = 30.0

    @property
    def speech_enabled(self) -> bool:
        return bool(self.elevenlabs_api_key)

    # --- OCR ---------------------------------------------------------------
    # "auto" tries local OCR then AI vision; "off" stores documents without
    # attempting to read them.
    ocr_provider: str = Field(default="auto", description="auto | local | ai | off")
    ocr_timeout_seconds: float = 60.0

    # --- Storage -----------------------------------------------------------
    upload_dir: Path = BACKEND_ROOT / "var" / "uploads"
    max_upload_bytes: int = 10 * 1024 * 1024

    # --- Visit handoff -----------------------------------------------------
    # Where the web app is served, used to build the link inside the handoff
    # QR code. Unset means the code carries the visit data itself instead,
    # which works with no network but holds less.
    public_web_url: str | None = None
    # A handoff link is a capability: whoever holds it can read that one
    # visit. It is meant to live only as long as the consultation, so it
    # expires quickly and the patient can always show a fresh code.
    handoff_link_ttl_minutes: int = 30

    @property
    def handoff_links_enabled(self) -> bool:
        return bool(self.public_web_url)

    # --- CORS --------------------------------------------------------------
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @property
    def is_testing(self) -> bool:
        return self.environment == "test"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
