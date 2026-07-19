# Backend

FastAPI application with async SQLAlchemy, Alembic migrations, JWT authentication, and Taskiq background workers.

## Setup

```bash
uv sync
cp .env.example .env  # edit as needed
uv run fastapi dev src/main.py --reload
```

## Running Tests

```bash
make test         # Run tests
make coverage     # With coverage report
```
