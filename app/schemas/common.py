"""
Common/shared response schemas used across the entire API.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """Standard envelope for all API responses."""
    success: bool = True
    message: str = "OK"
    data: T | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    success: bool = True
    message: str = "OK"
    data: list[T] = []
    total: int = 0
    page: int = 1
    per_page: int = 20


class MessageResponse(BaseModel):
    """Simple message response."""
    success: bool = True
    message: str = "OK"
