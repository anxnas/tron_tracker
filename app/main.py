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


@app.on_event("startup")
async def startup_event():
    """Выполняется при запуске приложения."""
    log.info("Приложение запущено")


@app.on_event("shutdown")
async def shutdown_event():
    """Выполняется при остановке приложения."""
    log.info("Приложение остановлено")


@app.get("/health")
async def health_check():
    """Проверка работоспособности приложения."""
    return {"status": "ok"}