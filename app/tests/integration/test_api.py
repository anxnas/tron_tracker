import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.services import TronService
from app.models import AddressQuery


@pytest.mark.asyncio
async def test_get_address_info(client: TestClient, mock_tron_data, test_db):
    """Тест эндпоинта получения информации об адресе."""

    # Мокаем метод получения информации о адресе с использованием AsyncMock
    with patch.object(
            TronService,
            'get_address_info',
            new_callable=AsyncMock,  # Важно использовать AsyncMock для асинхронных методов
            return_value=mock_tron_data
    ) as mock_get_info:
        # Отправляем запрос к API
        response = client.post(
            "/api/v1/tron/address",
            json={"address": mock_tron_data["address"]}
        )

        # Проверяем, что запрос успешно обработан
        assert response.status_code == 200
        assert response.json() == mock_tron_data

        # Проверяем, что метод получения информации был вызван с правильными параметрами
        mock_get_info.assert_called_once_with(mock_tron_data["address"])

        # Проверяем, что запись была добавлена в БД
        test_db.commit()  # Явно вызываем commit для гарантии сохранения

        # Используем прямой запрос вместо вложенного
        query_result = test_db.query(AddressQuery).filter_by(address=mock_tron_data["address"]).first()
        assert query_result is not None
        assert query_result.address == mock_tron_data["address"]
        assert query_result.bandwidth == mock_tron_data["bandwidth"]
        assert query_result.energy == mock_tron_data["energy"]
        assert query_result.balance == mock_tron_data["balance"]


@pytest.mark.asyncio
async def test_get_address_history(client: TestClient, mock_tron_data, test_db):
    """Тест эндпоинта получения истории запросов."""

    # Добавляем тестовые данные в БД
    for i in range(15):
        address_query = AddressQuery(
            address=f"{mock_tron_data['address']}{i}",
            bandwidth=mock_tron_data["bandwidth"],
            energy=mock_tron_data["energy"],
            balance=mock_tron_data["balance"]
        )
        test_db.add(address_query)
    test_db.commit()

    # Отправляем запрос к API
    response = client.get("/api/v1/tron/history?page=1&limit=10")

    # Проверяем, что запрос успешно обработан
    assert response.status_code == 200

    # Проверяем структуру ответа
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "pages" in data

    # Проверяем пагинацию
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["pages"] == 2
    assert len(data["items"]) == 10
    assert data["next_page"] == 2
    assert data["prev_page"] is None

    # Проверяем вторую страницу
    response = client.get("/api/v1/tron/history?page=2&limit=10")
    data = response.json()
    assert len(data["items"]) == 5
    assert data["next_page"] is None
    assert data["prev_page"] == 1