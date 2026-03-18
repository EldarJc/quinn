ARG PYTHON_VERSION=3.12.10
FROM python:${PYTHON_VERSION}-slim as builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry "poetry>=2.0.0,<3.0.0"
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root


FROM python:${PYTHON_VERSION}-slim as base

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser:appuser /app


COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser ./ /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
