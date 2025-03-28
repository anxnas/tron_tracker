import pytest
from app.repositories import AddressRepository
from app.models import AddressQuery
from app.schemas import PaginationParams


def test_create_address_query(test_db):
    """Тест создания записи о запросе адреса."""

    # Тестовые данные
    address_data = {
        "address": "TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W",
        "bandwidth": "5000",
        "energy": "2000",
        "balance": "100.5"
    }

    # Создаем репозиторий
    repository = AddressRepository(test_db)

    # Создаем запись
    result = repository.create(address_data)

    # Проверяем, что запись создана и содержит правильные данные
    assert result.address == address_data["address"]
    assert result.bandwidth == address_data["bandwidth"]
    assert result.energy == address_data["energy"]
    assert result.balance == address_data["balance"]

    # Проверяем, что запись сохранена в БД
    db_record = test_db.query(AddressQuery).filter_by(id=result.id).first()
    assert db_record is not None
    assert db_record.address == address_data["address"]


def test_get_history_with_pagination(test_db):
    """Тест получения истории запросов с пагинацией."""

    # Добавляем тестовые данные в БД
    for i in range(15):
        address_query = AddressQuery(
            address=f"TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W{i}",
            bandwidth="5000",
            energy="2000",
            balance="100.5"
        )
        test_db.add(address_query)
    test_db.commit()

    # Создаем репозиторий
    repository = AddressRepository(test_db)

    # Получаем первую страницу
    pagination = PaginationParams(page=1, limit=10)
    result = repository.get_history(pagination)

    # Проверяем результаты
    assert result["total"] == 15
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["pages"] == 2
    assert len(result["items"]) == 10
    assert result["next_page"] == 2
    assert result["prev_page"] is None

    # Получаем вторую страницу
    pagination = PaginationParams(page=2, limit=10)
    result = repository.get_history(pagination)

    # Проверяем результаты
    assert len(result["items"]) == 5
    assert result["next_page"] is None
    assert result["prev_page"] == 1