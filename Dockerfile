FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей для сборки пакетов
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt

# Копирование кода приложения
COPY . .

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]