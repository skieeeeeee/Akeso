"""Application error types and the JSON error contract.

Patients must never see a raw traceback or a database message, so every
failure leaves the API as `{"error": {"code", "message", "details"}}` with a
human-readable message.
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings


class AppError(HTTPException):
    """Base class for expected, client-visible failures."""

    code = "app_error"

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any = None,
        code: str | None = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.details = details
        if code:
            self.code = code


class NotFoundError(AppError):
    code = "not_found"

    def __init__(self, what: str = "Resource", details: Any = None) -> None:
        super().__init__(
            f"{what} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationFailedError(AppError):
    code = "validation_failed"

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details
        )


class ConflictError(AppError):
    code = "conflict"

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message, status_code=status.HTTP_409_CONFLICT, details=details
        )


class AuthenticationError(AppError):
    code = "authentication_failed"

    def __init__(self, message: str = "Please sign in again to continue.") -> None:
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class UpstreamUnavailableError(AppError):
    """A dependency (mock ABHA, OCR, AI provider) could not be reached.

    Always paired with a usable fallback in the calling feature.
    """

    code = "upstream_unavailable"

    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, details=details
        )


# Pydantic prefixes messages raised from validators; patients should not see it.
_PYDANTIC_PREFIXES = ("Value error, ", "Assertion failed, ")


def safe_details(errors: list[Any]) -> list[dict[str, Any]]:
    """Strip anything unserialisable out of Pydantic's error list.

    `errors()` embeds the original exception object under `ctx`, which cannot
    be JSON-encoded — serialising it raw turns a 422 into a 500.
    """
    cleaned: list[dict[str, Any]] = []
    for error in errors:
        entry = {
            "type": str(error.get("type", "")),
            "loc": [str(part) for part in error.get("loc", [])],
            "msg": str(error.get("msg", "")),
        }
        ctx = error.get("ctx")
        if isinstance(ctx, dict):
            entry["ctx"] = {key: str(value) for key, value in ctx.items()}
        cleaned.append(entry)
    return cleaned


def first_validation_message(errors: list[Any]) -> str:
    """Turn Pydantic's error list into one message a patient can act on.

    Our own validators raise `ValueError` with patient-readable text, so the
    specific message survives instead of being replaced by a generic one.
    """
    for error in errors:
        message = str(error.get("msg", "")).strip()
        for prefix in _PYDANTIC_PREFIXES:
            if message.startswith(prefix):
                return message[len(prefix) :]
    for error in errors:
        if error.get("type") == "value_error":
            return str(error.get("msg", "")).strip()
    # Fall back to naming the offending field when the message is generic.
    for error in errors:
        location = [str(part) for part in error.get("loc", []) if part != "body"]
        if location:
            field = location[-1].replace("_", " ")
            return f"Please check the {field} field and try again."
    return "Please check the highlighted fields and try again."


def persist_before_raise(db: Any) -> None:
    """Commit work that must survive the error about to be raised.

    The request-scoped session rolls back on any exception, which would
    otherwise discard security-relevant state such as a failed-attempt
    counter, or input we promised to preserve for the patient.
    """
    db.commit()


def _envelope(code: str, message: str, details: Any = None) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "details": details}}


def register_error_handlers(app: Any) -> None:
    """Attach handlers so no unexpected exception reaches a patient raw."""

    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(HTTPException)
    async def _http_error(request: Request, exc: HTTPException) -> Any:
        if isinstance(exc, AppError):
            return await _app_error(request, exc)
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope("http_error", message),
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(ValidationError)
    async def _pydantic_error(_: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope(
                "validation_failed",
                first_validation_message(exc.errors()),
                safe_details(exc.errors()),
            ),
        )

    @app.exception_handler(SQLAlchemyError)
    async def _db_error(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        # Never surface SQL to a patient.
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=_envelope(
                "database_unavailable",
                "We could not save your information just now. Please try again.",
                str(exc) if settings.debug else None,
            ),
        )

    @app.exception_handler(Exception)
    async def _unexpected(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope(
                "internal_error",
                "Something went wrong on our side. Please try again.",
                str(exc) if settings.debug else None,
            ),
        )

    # Keep FastAPI's own 422 shape aligned with ours.
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def _request_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_envelope(
                "validation_failed",
                first_validation_message(exc.errors()),
                safe_details(exc.errors()),
            ),
        )

    _ = http_exception_handler  # imported for parity with FastAPI defaults
