"""FastAPI application factory."""

from __future__ import annotations

from fastapi import APIRouter, FastAPI
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
    ):
        api.include_router(module_router)
    return api


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
    )

    register_error_handlers(app)
    app.include_router(build_router())

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name, "environment": settings.environment}

    return app


app = create_app()
