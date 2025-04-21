# Этап сборки
FROM python:3.14-rc AS builder

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Установка зависимостей Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1

# Добавление Poetry в PATH
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

# Создание директории для приложения и установка зависимостей
WORKDIR /code
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости с помощью Poetry
RUN poetry install --no-dev --no-interaction --no-ansi


# Этап запуска
FROM python:3.14-rcpython:3.11-slim AS runtime

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

EXPOSE 8000

COPY ./config ./config
COPY ./app ./app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "app.main"]
