FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PRE_COMMIT_HOME=/tmp/pre-commit-cache

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends git libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m pip install pre-commit && pre-commit install