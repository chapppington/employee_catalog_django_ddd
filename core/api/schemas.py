from typing import (
    Any,
    Generic,
    TypeVar,
)

from ninja import Schema

from core.api.filters import PaginationOut


TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


class PingResponseSchema(Schema):
    response: bool


class ListPaginatedResponse(Schema, Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOut


class ApiResponse(Schema, Generic[TData]):
    data: TData | dict = {}
    meta: dict[str, Any] = {}
    errors: list[Any] = []
