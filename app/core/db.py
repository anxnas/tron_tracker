from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

from app.config import settings
from app.utils import log
from app.exceptions import DatabaseError

# Создаем соединение с базой данных
engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()


def get_db() -> Generator:
    """
    Зависимость для FastAPI, которая предоставляет сессию БД.

    Yields:
        Session: Сессия SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        log.error(f"Ошибка при работе с БД: {str(e)}")
        raise DatabaseError(f"Ошибка при работе с базой данных: {str(e)}")
    except Exception as e:
        db.rollback()
        log.error(f"Неожиданная ошибка при работе с БД: {str(e)}")
        raise DatabaseError(f"Неожиданная ошибка при работе с базой данных: {str(e)}")
    finally:
        db.close()