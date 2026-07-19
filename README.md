# FastAPI Async Starter

Starter template for FastAPI projects with async SQLAlchemy, Alembic, JWT auth, Taskiq background workers, and Docker Compose.

## Quick Start

```bash
docker compose -f compose.yml -f compose.local.yml up --build
```

API at `http://localhost:8000`, OpenAPI docs at `http://localhost:8000/docs`.

## Services (Docker)

| Service | Description                   | Port |
|---------|-------------------------------|------|
| backend | FastAPI application           | 8000 |
| worker  | Taskiq background task worker |      |
| db      | PostgreSQL 18                 | 5432 |
| valkey  | Valkey 8 (Redis-compatible)   | 6379 |

## Project Structure

```
backend/src/
├── core/                # config, constants, exceptions
├── db/                  # engine, models, seed
├── extensions/          # lifespan, logs, middleware, error handlers
├── modules/             # Your app domains go here
│   └── items/           # example CRUD module
├── auth/                # JWT utilities
├── users/               # user management + auth
├── workers/             # background tasks
├── router.py            # route registration
├── utils.py             # shared helpers
└── main.py              # app factory
```

## Adding a New Module

1. Copy `src/modules/items/` to `src/modules/<name>/`
2. Register in `src/router.py`
3. Import model in `alembic/env.py`
4. Generate migration: `make migrate`

## Configuration

| Variable                 | Default                                           |
|--------------------------|---------------------------------------------------|
| `POSTGRES_USER`          | `app`                                             |
| `POSTGRES_PASSWORD`      | `app`                                             |
| `POSTGRES_DB`            | `app`                                             |
| `DATABASE_URL`           | `postgresql+asyncpg://app:app@localhost:5432/app` |
| `ENVIRONMENT`            | `local`                                           |
| `CORS_ORIGINS`           | `["http://localhost:4321"]`                       |
| `AUTH_JWT_SECRET`        | (change in production)                            |
| `AUTH_REFRESH_TOKEN_KEY` | (change in production)                            |

## Commands

```bash
make lint     # Ruff check
make test     # Run tests
make dev      # Run dev server
make migrate  # Generate migration
```

## Stack

**Python 3.14** · **FastAPI** · **SQLAlchemy 2.0** (async) · **Pydantic v2**
**Alembic** · **Taskiq** + Valkey · **Structlog**
**PostgreSQL 18** · **Valkey 8** · **Docker** · **Ruff** · **pytest**

## Acknowledgments

This project draws on the patterns and conventions from
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
by [zhanymkanov](https://github.com/zhanymkanov) and the reference implementation shared by
[ccrvlh](https://github.com/ccrvlh) in
[issue #4](https://github.com/zhanymkanov/fastapi-best-practices/issues/4).
