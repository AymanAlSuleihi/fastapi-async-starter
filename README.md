# FastAPI Async Starter

Modular asynchronous FastAPI starter project with all the basics for building a scalable and maintainable web application with a PostgreSQL database, background task processing, and JWT authentication.

## Tech

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-1.13-6C757D?logo=alembic&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
![Taskiq](https://img.shields.io/badge/Taskiq-0.11-FF6F00)
![Valkey](https://img.shields.io/badge/Valkey-8-9254DE?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-✓-DEB887)
![Ruff](https://img.shields.io/badge/Ruff-0.6-D7FF64?logo=ruff&logoColor=black)
![Ty](https://img.shields.io/badge/Ty-0.0.55-FF6F00?logo=ty&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-✓-0A9EDC?logo=pytest&logoColor=white)

## Quick Start

```bash
# Copy the example environment file to `.env`
cp .env.example .env

# Generate a new secret key for JWT auth and set it in `.env`
openssl rand -hex 32

# Generate a second secret key for refresh tokens and set it in `.env`
openssl rand -hex 32

# Update the values in `.env` as needed (e.g., database credentials, superuser, CORS origins, etc.)
vi .env
# or
nano .env

# If running locally, review `.env.local` and update the values as needed
vi .env.local
# or
nano .env.local

# Start the application with Docker Compose
# Local development
docker compose -f compose.yml -f compose.local.yml up --build

# Production
docker compose -f compose.yml up --build

# To stop the application
docker compose down
```

API at `http://localhost:8000`, OpenAPI docs at `http://localhost:8000/docs`.

## Services (Docker)

| Service | Description                   | Port |
|---------|-------------------------------|------|
| backend | FastAPI application           | 8000 |
| db      | PostgreSQL 18                 | 5432 |
| worker  | Taskiq background task worker |      |
| valkey  | Valkey 8 (Redis-compatible)   | 6379 |

## Project Structure

```
backend/src/
├── core/                # config, constants, exceptions
├── db/                  # engine, models, seed
├── extensions/          # logs, middleware, error handlers
├── services/            # infrastructure clients (mailer, storage, etc.)
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
4. Generate migration: `cd backend && make migrate`

## Commands

All commands assume you are in the `backend/` directory.

```bash
make lint     # Ruff check
make fix      # Ruff fix
make format   # Autoformat code
make type     # Type check
make test     # Run tests
make coverage # Run tests with coverage
make all      # Run all checks
make dev      # Run dev server
make migrate  # Generate migration
make dump     # Dump database
make restore  # Restore database
```

### Apply migrations

```bash
docker compose exec backend alembic upgrade head
```

## Contributions

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgments

This project draws on the patterns and conventions from
[fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)
by [zhanymkanov](https://github.com/zhanymkanov) and the reference implementation shared by
[ccrvlh](https://github.com/ccrvlh) in
[issue #4](https://github.com/zhanymkanov/fastapi-best-practices/issues/4).
