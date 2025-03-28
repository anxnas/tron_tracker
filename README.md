# TRON Tracker - Микросервис для получения информации о TRON-адресах

Этот микросервис предоставляет API для получения информации о TRON-адресах, включая bandwidth, energy и баланс TRX, и сохраняет историю запросов в базе данных.

## Функциональность

- Получение информации о TRON-адресе (bandwidth, energy, баланс TRX)
- Сохранение всех запросов в базе данных
- Получение истории запросов с пагинацией

## Технический стек

- FastAPI - асинхронный веб-фреймворк
- SQLAlchemy - ORM для работы с базой данных
- PostgreSQL - база данных
- tronpy - библиотека для работы с TRON API
- Pydantic - валидация и сериализация данных
- Pytest - тестирование
- Docker - контейнеризация

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.10+

### Локальная разработка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/anxnas/tron_tracker.git
   cd tron_tracker
   ```

2. Создать виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   # или
   venv\Scripts\activate  # для Windows
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements/dev.txt
   ```

4. Создать файл .env на основе example.env:
   ```bash
   cp .env.example .env
   ```

5. Настроить переменные окружения в файле .env

6. Инициализировать базу данных:
   ```bash
   alembic revision --autogenerate -m "Initial db"
   ```

7. Применить миграции:
   ```bash
   alembic upgrade head
   ```

8. Запустить приложение:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

9. Перейти по адресу [http://localhost:8000/docs](http://localhost:8000/docs) для просмотра документации API

### Запуск с использованием Docker

1. Создать файл .env на основе .env.example:
   ```bash
   cp .env.example .env
   ```

2. Настроить переменные окружения в файле .env

3. Запустить приложение с помощью Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Перейти по адресу [http://localhost/docs](http://localhost/docs) для просмотра документации API

## API Endpoints

### 1. Получение информации о TRON-адресе

**POST** `/api/v1/tron/address`

Получение информации о TRON-адресе и сохранение запроса в БД.

**Запрос**:
```json
{
  "address": "TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W"
}
```

**Ответ**:
```json
{
  "address": "TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W",
  "bandwidth": "5000",
  "energy": "2000",
  "balance": "100.5"
}
```

### 2. Получение истории запросов с пагинацией

**GET** `/api/v1/tron/history?page=1&limit=10`

Получение истории запросов с пагинацией.

**Параметры запроса**:
- `page` - номер страницы (начиная с 1)
- `limit` - количество элементов на странице (от 1 до 100)

**Ответ**:
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "address": "TJ8RoHsTnHdUGtrvXZtzP7GdYB4DW3ct9W",
      "bandwidth": "5000",
      "energy": "2000",
      "balance": "100.5",
      "created_at": "2023-07-31T15:30:45.123456"
    },
    ...
  ],
  "total": 100,
  "page": 1,
  "limit": 10,
  "pages": 10,
  "next_page": 2,
  "prev_page": null
}
```

## Тестирование

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov=api

# Запуск конкретного теста
pytest app/tests/unit/test_repositories.py

```

### Тесты

- Интеграционные тесты API:
  - Проверка получения информации о TRON-адресе
  - Проверка получения истории запросов с пагинацией

- Юнит-тесты:
  - Проверка создания записи о запросе адреса в репозитории
  - Проверка получения истории запросов с пагинацией

## Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для получения дополнительной информации.

## Контакты

- Разработчик: anxnas (Хренов Святослав Валерьевич)
- Тг канал: https://t.me/anxnas

2025 год
