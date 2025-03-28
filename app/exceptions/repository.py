from app.exceptions.base import DatabaseError, NotFoundError, ValidationError
from fastapi import status


class RecordNotFoundError(NotFoundError):
    """Исключение для случаев, когда запись не найдена в БД."""

    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Запись не найдена в базе данных"


class DatabaseOperationError(DatabaseError):
    """Исключение для ошибок операций с базой данных."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "Ошибка при выполнении операции с базой данных"


class InvalidPaginationError(ValidationError):
    """Исключение для ошибок пагинации."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Недопустимые параметры пагинации"