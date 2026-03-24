"""
Custom exception classes and global exception handlers for the application.
"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


# ── Domain Exceptions ────────────────────────────────────


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str = "Terjadi kesalahan internal."):
        self.message = message
        super().__init__(self.message)


class NotFoundException(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str, identifier: int | str):
        super().__init__(f"{resource} dengan ID {identifier} tidak ditemukan.")
        self.resource = resource
        self.identifier = identifier


class DuplicateException(AppException):
    """Raised when attempting to create a duplicate resource."""

    def __init__(self, resource: str, detail: str = ""):
        message = f"Data {resource} sudah ada."
        if detail:
            message += f" {detail}"
        super().__init__(message)


class ValidationException(AppException):
    """Raised when business‑rule validation fails."""

    def __init__(self, message: str):
        super().__init__(message)


class AlgorithmException(AppException):
    """Raised when the scheduling algorithm encounters an error."""

    def __init__(self, message: str = "Gagal menjalankan algoritma."):
        super().__init__(message)


# ── HTTP Exception Handlers ─────────────────────────────


async def not_found_handler(_: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "message": exc.message},
    )


async def duplicate_handler(_: Request, exc: DuplicateException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"success": False, "message": exc.message},
    )


async def validation_handler(_: Request, exc: ValidationException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": exc.message},
    )


async def algorithm_handler(_: Request, exc: AlgorithmException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": exc.message},
    )


async def generic_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": exc.message},
    )


# ── Registry (used by main.py) ──────────────────────────

EXCEPTION_HANDLERS: dict[type[Exception], object] = {
    NotFoundException: not_found_handler,
    DuplicateException: duplicate_handler,
    ValidationException: validation_handler,
    AlgorithmException: algorithm_handler,
    AppException: generic_handler,
}
