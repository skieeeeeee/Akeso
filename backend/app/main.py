"""FastAPI application factory."""

from __future__ import annotations

from fastapi import APIRouter, FastAPI
import logging

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.shared.errors import register_error_handlers

# Importing the metadata module registers every model on the shared Base.
from app.database import metadata as _metadata  # noqa: F401


def build_router() -> APIRouter:
    """Compose the versioned API from each module's router.

    Modules are mounted here and nowhere else, so the API surface is
    reviewable in one place.
    """
    from app.modules.abha.router import router as abha_router
    from app.modules.ayush.router import router as ayush_router
    from app.modules.interview.router import router as interview_router
    from app.modules.timeline.router import router as timeline_router
    from app.modules.accessibility.router import router as accessibility_router
    from app.modules.auth.router import router as auth_router
    from app.modules.consent.router import router as consent_router
    from app.modules.encounter.router import router as encounter_router
    from app.modules.documents.router import router as documents_router
    from app.modules.medical_history.router import router as medical_history_router
    from app.modules.patient.router import router as patient_router
    from app.modules.speech.router import router as speech_router

    api = APIRouter(prefix=settings.api_prefix)
    for module_router in (
        auth_router,
        patient_router,
        abha_router,
        accessibility_router,
        consent_router,
        medical_history_router,
        documents_router,
        interview_router,
        ayush_router,
        timeline_router,
        encounter_router,
        speech_router,
    ):
        api.include_router(module_router)
    return api


def _warn_about_prototype_auth() -> None:
    """Say plainly, at every startup, that sign-in is not real.

    Both of these are deliberate prototype affordances, and both mean anyone
    who knows a mobile number can read that patient's record. A deployment
    that leaves them on should have to see this in its logs.
    """
    log = logging.getLogger("medikiosk.startup")
    if settings.dev_fixed_otp:
        log.warning(
            "PROTOTYPE: every mobile number accepts the fixed code %r. "
            "Set DEV_FIXED_OTP=\"\" before real patients can sign in.",
            settings.dev_fixed_otp,
        )
    if settings.expose_mock_otp:
        log.warning(
            "PROTOTYPE: the one-time code is returned in the API response. "
            "Set EXPOSE_MOCK_OTP=false before real patients can sign in."
        )
    if settings.jwt_secret.startswith("dev-only"):
        log.warning(
            "PROTOTYPE: JWT_SECRET is still the development default. "
            "Generate one before deploying anywhere reachable."
        )


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.app_name} API",
        version="0.1.0",
        description=(
            "Patient case-taking and medical history platform. "
            "Phase 1: onboarding, accessibility and patient profile."
        ),
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # A browser cannot read a response header cross-origin unless it is
        # named here, and the handoff screen needs this one to know whether
        # the code it just fetched carries a link or the visit data — which
        # decides what it tells the patient will happen when it is scanned.
        expose_headers=["X-Handoff-Kind"],
    )

    _warn_about_prototype_auth()

    register_error_handlers(app)
    app.include_router(build_router())

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name, "environment": settings.environment}

    return app


app = create_app()
