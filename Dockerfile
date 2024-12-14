# Этап сборки

FROM python:3.11-slim AS builder

#RUN apt-get update && apt-get install -y curl build-essential libpq-dev \
#    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \

# Установка зависимостей Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry self update 1.8.0

# Добавление Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Создание директории для приложения и установка зависимостей
WORKDIR /code
COPY pyproject.toml poetry.lock /code/

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi


# Этап запуска
FROM python:3.11-slim AS runtime

WORKDIR /code

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

COPY --from=builder /code /code

EXPOSE 8000

COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["poetry", "run", "python", "-m", "app.main"]
