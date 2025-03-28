from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения."""

    # Основные настройки
    APP_NAME: str = "TRON Tracker"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Настройки логирования
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Настройки базы данных
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "tron_tracker"

    # Настройки TRON API
    TRON_API_KEY: Optional[str] = None

    @property
    def DATABASE_URI(self) -> str:
        """
        Формирует строку подключения к БД на основе настроек.

        Returns:
            str: URI для подключения к базе данных
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()