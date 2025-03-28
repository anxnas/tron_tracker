from typing import TypeVar, Generic, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.base import BaseModel
from app.exceptions import RecordNotFoundError, DatabaseOperationError
from app.utils import log

T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    """Базовый репозиторий для работы с моделями."""

    def __init__(self, db: Session, model: Type[T]):
        """
        Инициализация репозитория.

        Args:
            db: Сессия SQLAlchemy
            model: Класс модели
        """
        self.db = db
        self.model = model

    def get_by_id(self, id: Any) -> T:
        """
        Получение записи по ID.

        Args:
            id: Идентификатор записи

        Returns:
            T: Запись

        Raises:
            RecordNotFoundError: Если запись не найдена
        """
        try:
            record = self.db.query(self.model).filter(self.model.id == id).first()
            if not record:
                raise RecordNotFoundError(f"Запись {self.model.__name__} с id={id} не найдена")
            return record
        except SQLAlchemyError as e:
            log.error(f"Ошибка при получении записи по ID: {str(e)}")
            raise DatabaseOperationError(f"Ошибка при получении записи: {str(e)}")

    def create(self, data: Dict[str, Any]) -> T:
        """
        Создание новой записи.

        Args:
            data: Данные для создания записи

        Returns:
            T: Созданная запись

        Raises:
            DatabaseOperationError: При ошибке создания записи
        """
        try:
            obj = self.model(**data)
            self.db.add(obj)
            self.db.flush()
            return obj
        except SQLAlchemyError as e:
            log.error(f"Ошибка при создании записи: {str(e)}")
            raise DatabaseOperationError(f"Ошибка при создании записи: {str(e)}")