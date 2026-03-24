from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):

    success: bool = True

    message: str = "OK"

    data: T | None = None

class PaginatedResponse(BaseModel, Generic[T]):

    success: bool = True

    message: str = "OK"

    data: list[T] = []

    total: int = 0

    page: int = 1

    per_page: int = 20

class MessageResponse(BaseModel):

    success: bool = True

    message: str = "OK"
