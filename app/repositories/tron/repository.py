from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any

from app.repositories.base import BaseRepository
from app.models import AddressQuery
from app.schemas import PaginationParams
from app.exceptions import DatabaseOperationError, InvalidPaginationError
from app.utils import log


class AddressRepository(BaseRepository[AddressQuery]):
    """Репозиторий для работы с запросами TRON-адресов."""

    def __init__(self, db):
        """
        Инициализация репозитория.

        Args:
            db: Сессия SQLAlchemy
        """
        super().__init__(db, AddressQuery)

    def get_history(self, pagination: PaginationParams) -> Dict[str, Any]:
        """
        Получение истории запросов с пагинацией.

        Args:
            pagination: Параметры пагинации

        Returns:
            Dict: Результаты с пагинацией

        Raises:
            InvalidPaginationError: При некорректных параметрах пагинации
            DatabaseOperationError: При ошибке работы с БД
        """
        try:
            # Проверка корректности параметров пагинации
            if pagination.page < 1 or pagination.limit < 1:
                raise InvalidPaginationError("Некорректные параметры пагинации: page и limit должны быть больше 0")

            query = self.db.query(self.model).order_by(desc(self.model.created_at))

            # Подсчет общего количества
            total = query.count()

            # Проверка, что запрашиваемая страница существует
            pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 1
            if pagination.page > pages and total > 0:
                raise InvalidPaginationError(f"Запрашиваемая страница не существует: доступно {pages} страниц")

            # Вычисление смещения для пагинации
            skip = (pagination.page - 1) * pagination.limit

            # Получение элементов для текущей страницы
            items = query.offset(skip).limit(pagination.limit).all()

            # Определение следующей и предыдущей страницы
            next_page = pagination.page + 1 if pagination.page < pages else None
            prev_page = pagination.page - 1 if pagination.page > 1 else None

            return {
                "items": items,
                "total": total,
                "page": pagination.page,
                "limit": pagination.limit,
                "pages": pages,
                "next_page": next_page,
                "prev_page": prev_page
            }
        except InvalidPaginationError:
            # Пробрасываем уже созданные исключения
            raise
        except SQLAlchemyError as e:
            log.error(f"Ошибка при получении истории запросов: {str(e)}")
            raise DatabaseOperationError(f"Ошибка при получении истории запросов: {str(e)}")