# Этап сборки

FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y curl

# Установка зависимостей Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1

# Добавление Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Создание директории для приложения и установка зависимостей
WORKDIR /code
COPY pyproject.toml poetry.lock /code/

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install


# Этап запуска
FROM python:3.11-slim AS runtime

COPY --from=builder /code .

EXPOSE 8000

COPY . .

CMD ["poetry", "run", "python", "-m", "app.main"]
# # ###CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
