from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.exceptions import BaseAppException
from app.utils import log


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware для перехвата и обработки исключений."""

    async def dispatch(self, request: Request, call_next):
        """
        Перехватывает исключения и возвращает соответствующий ответ.

        Args:
            request: HTTP-запрос
            call_next: Следующий обработчик

        Returns:
            Response: HTTP-ответ
        """
        try:
            return await call_next(request)
        except BaseAppException as e:
            # Обрабатываем кастомные исключения приложения
            log.error(f"Обработано исключение: {type(e).__name__}: {str(e)}")
            return JSONResponse(
                status_code=e.status_code,
                content={"message": e.message, "detail": e.detail if e.detail else None}
            )
        except Exception as e:
            # Обрабатываем необработанные исключения
            log.error(f"Необработанное исключение: {type(e).__name__}: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"message": "Внутренняя ошибка сервера", "detail": str(e)}
            )