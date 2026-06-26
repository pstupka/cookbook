# Cookbook API

REST API for the Cookbook app, built with FastAPI, SQLAlchemy, and PostgreSQL.

## Requirements

- Python 3.12+
- Docker & Docker Compose

## Setup

1. Copy the environment file and fill in your values:
   ```bash
   cp .env.example .env
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running

```bash
# Start the database
docker compose -f ../docker-compose.dev.yml up -d db

# Apply migrations
alembic upgrade head

# Start the API (hot reload)
uvicorn app.main:app --reload
```

API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Database migrations

```bash
# Generate a migration after changing models
alembic revision --autogenerate -m "description"

# Apply pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```

## Testing

```bash
pytest
```

Tests use an in-memory SQLite database and do not require a running Postgres instance.

## Seeding

Populate the database with example data:

```bash
docker compose -f ../docker-compose.dev.yml run --rm api python seed.py
```

This creates an `admin` user (password: `secret`) and two sample recipes.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/recipes` | List recipes |
| POST | `/api/v1/recipes` | Create recipe |
| GET | `/api/v1/recipes/{id}` | Get recipe |
| PUT | `/api/v1/recipes/{id}` | Update recipe |
| DELETE | `/api/v1/recipes/{id}` | Delete recipe |
| GET | `/api/v1/ingredients` | List ingredients |
| POST | `/api/v1/ingredients` | Create ingredient |
| PATCH | `/api/v1/ingredients/{id}` | Update ingredient |
| DELETE | `/api/v1/ingredients/{id}` | Delete ingredient |
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users/{id}` | Get user |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |