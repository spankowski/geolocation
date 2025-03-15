FROM python:3.12.6-slim-bookworm

# Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy dependency files first to leverage Docker caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies (including uvicorn)
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app

# Explicitly use uvicorn as the command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]