FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .


FROM python:3.12-slim

RUN useradd --no-create-home --shell /bin/false appuser

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini .
COPY tasks/purge_db.py .
COPY tasks/seed.py .
COPY tasks/init_admin.py .

USER appuser

CMD ["sh", "-c", "alembic upgrade head && python init_admin.py && uvicorn app.main:app --host 0.0.0.0 --workers 4"]