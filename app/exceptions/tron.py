from app.exceptions.base import APIError
from fastapi import status


class TronAPIException(APIError):
    """Исключение для ошибок TRON API."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Ошибка при обращении к TRON API"


class TronAddressNotFoundException(TronAPIException):
    """Исключение, когда адрес TRON не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Указанный TRON-адрес не найден"


class TronNetworkException(TronAPIException):
    """Исключение для ошибок сети при обращении к TRON API."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = "Ошибка сети при обращении к TRON API"