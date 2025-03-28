from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .config import settings
from .utils import log, setup_logging
from .middleware import ErrorHandlerMiddleware

# Настройка логирования
setup_logging()

# Создание экземпляра приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="API для получения информации о TRON-адресах",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене нужно указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем middleware для обработки ошибок
app.add_middleware(ErrorHandlerMiddleware)

# Подключение роутеров
app.include_router(api_router, prefix="/api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер жизненного цикла приложения.

    Обрабатывает события запуска и завершения работы приложения.
    """
    log.info("Приложение запущено")
    yield
    log.info("Приложение остановлено")


@app.get("/health")
async def health_check():
    """Проверка работоспособности приложения."""
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }