from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app.core.db import get_db
from app.schemas import (
    AddressRequest,
    TronAddressInfo,
    AddressQueryResponse,
    PaginationParams,
    PaginatedResponse
)
from app.services import TronService
from app.repositories import AddressRepository
from app.utils import log
from app.exceptions import (
    BaseAppException,
    TronAPIException,
    TronAddressNotFoundException,
    TronNetworkException,
    DatabaseOperationError,
    InvalidPaginationError
)

router = APIRouter()


@router.post("/address", response_model=TronAddressInfo)
async def get_address_info(
        request: AddressRequest,
        db: Session = Depends(get_db)
) -> Any:
    """
    Получение информации о TRON-адресе и сохранение запроса в БД.

    Args:
        request: Данные запроса с адресом
        db: Сессия БД

    Returns:
        TronAddressInfo: Информация о адресе

    Raises:
        HTTPException: При ошибке обработки запроса
    """
    try:
        # Получаем информацию о адресе
        tron_service = TronService()
        address_info = await tron_service.get_address_info(request.address)

        # Сохраняем запрос в БД
        repository = AddressRepository(db)
        repository.create(address_info)

        log.info(f"Информация о адресе {request.address} успешно получена и сохранена")
        return address_info
    except TronAddressNotFoundException as e:
        log.warning(f"Адрес не найден: {str(e)}")
        raise e.to_http_exception()
    except TronNetworkException as e:
        log.error(f"Ошибка сети TRON: {str(e)}")
        raise e.to_http_exception()
    except TronAPIException as e:
        log.error(f"Ошибка TRON API: {str(e)}")
        raise e.to_http_exception()
    except DatabaseOperationError as e:
        log.error(f"Ошибка БД при сохранении запроса: {str(e)}")
        raise e.to_http_exception()
    except BaseAppException as e:
        log.error(f"Ошибка приложения: {str(e)}")
        raise e.to_http_exception()
    except Exception as e:
        log.error(f"Неожиданная ошибка при обработке запроса: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": f"Неожиданная ошибка при получении информации о адресе: {str(e)}"}
        )


@router.get("/history", response_model=PaginatedResponse[AddressQueryResponse])
async def get_address_history(
        pagination: PaginationParams = Depends(),
        db: Session = Depends(get_db)
) -> Any:
    """
    Получение истории запросов с пагинацией.

    Args:
        pagination: Параметры пагинации
        db: Сессия БД

    Returns:
        PaginatedResponse: Список записей с пагинацией

    Raises:
        HTTPException: При ошибке получения истории запросов
    """
    try:
        repository = AddressRepository(db)
        result = repository.get_history(pagination)

        log.info(f"Получена история запросов (страница {pagination.page}, лимит {pagination.limit})")
        return result
    except InvalidPaginationError as e:
        log.warning(f"Некорректные параметры пагинации: {str(e)}")
        raise e.to_http_exception()
    except DatabaseOperationError as e:
        log.error(f"Ошибка БД при получении истории: {str(e)}")
        raise e.to_http_exception()
    except BaseAppException as e:
        log.error(f"Ошибка приложения: {str(e)}")
        raise e.to_http_exception()
    except Exception as e:
        log.error(f"Неожиданная ошибка при получении истории запросов: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"message": f"Неожиданная ошибка при получении истории запросов: {str(e)}"}
        )