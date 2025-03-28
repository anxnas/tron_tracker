import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import Base, get_db
from app.main import app
from app.models import AddressQuery


# Настройка тестовой БД
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Включаем проверку внешних ключей для SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Переопределение зависимости БД для тестов
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()  # Добавляем явный commit
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def event_loop():
    """
    Создает экземпляр цикла событий для каждого теста.
    Необходимо для корректного использования pytest-asyncio.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db():
    """
    Создает тестовую базу данных с нужными таблицами и возвращает сессию.
    После выполнения теста очищает таблицы.
    """
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Удаляем таблицы
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """
    Создает тестовый клиент для запросов к API.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_tron_data():
    """
    Тестовые данные об адресе TRON.
    """
    return {
        "address": "TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W",
        "bandwidth": "5000",
        "energy": "2000",
        "balance": "100.5"
    }