FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1

ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

WORKDIR /code
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev --no-interaction --no-ansi


FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/code/.venv \
    PATH="/code/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}


COPY system_prompt.md ./
COPY ./src ./src

CMD ["python", "-m", "src.run"]
