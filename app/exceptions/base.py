from fastapi import HTTPException, status
from typing import Optional, Any, Dict


class BaseAppException(Exception):
    """Базовое исключение приложения."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = "Произошла внутренняя ошибка сервера"

    def __init__(
            self,
            message: Optional[str] = None,
            status_code: Optional[int] = None,
            detail: Optional[Dict[str, Any]] = None
    ):
        """
        Инициализация исключения.

        Args:
            message: Сообщение об ошибке
            status_code: Код статуса HTTP
            detail: Дополнительная информация об ошибке
        """
        self.message = message or self.default_message
        self.status_code = status_code or self.status_code
        self.detail = detail or {}
        super().__init__(self.message)

    def to_http_exception(self) -> HTTPException:
        """
        Преобразует исключение в HTTPException для FastAPI.

        Returns:
            HTTPException: Исключение для FastAPI
        """
        detail = {"message": self.message}
        if self.detail:
            detail["detail"] = self.detail
        return HTTPException(
            status_code=self.status_code,
            detail=detail
        )


class NotFoundError(BaseAppException):
    """Исключение для случаев, когда ресурс не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Запрашиваемый ресурс не найден"


class ValidationError(BaseAppException):
    """Исключение для ошибок валидации."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_message = "Ошибка валидации данных"


class APIError(BaseAppException):
    """Исключение для ошибок внешних API."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Ошибка при обращении к внешнему API"


class DatabaseError(BaseAppException):
    """Исключение для ошибок базы данных."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "Ошибка при работе с базой данных"