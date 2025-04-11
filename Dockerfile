FROM python:3.12-slim

RUN groupadd -r deploy && useradd -r -g deploy bot

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip && pip install "poetry==2.1.2"

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY . .

USER bot

EXPOSE 8000
CMD ["./entrypoint.sh"]