from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Параметры пагинации."""

    page: int = Field(1, ge=1, description="Номер страницы (начиная с 1)")
    limit: int = Field(10, ge=1, le=100, description="Количество элементов на странице")


class PaginatedResponse(BaseModel, Generic[T]):
    """Ответ с пагинацией."""

    items: List[T] = Field(..., description="Список элементов")
    total: int = Field(..., description="Общее количество элементов")
    page: int = Field(..., description="Текущая страница")
    limit: int = Field(..., description="Количество элементов на странице")
    pages: int = Field(..., description="Общее количество страниц")
    next_page: Optional[int] = Field(None, description="Номер следующей страницы")
    prev_page: Optional[int] = Field(None, description="Номер предыдущей страницы")