import os

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app:app@localhost:5432/app_test",
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL  # must be set before src imports

import pytest_asyncio  # noqa: E402
import sqlalchemy as sa  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa: E402

from src.db.engine import get_db  # noqa: E402
from src.db.models import Base  # noqa: E402
from src.main import app  # noqa: E402


async def _ensure_test_db(db_url: str) -> None:
    """Create the test database if it doesn't exist."""
    try:
        eng = create_async_engine(db_url, echo=False)
        async with eng.connect():
            return  # DB exists
    except Exception:
        pass

    # Connect to the "postgres" maintenance DB to create the test DB
    maint_url = db_url.rsplit("/", 1)[0] + "/postgres"
    maint_engine = create_async_engine(maint_url, echo=False, isolation_level="AUTOCOMMIT")
    try:
        async with maint_engine.connect() as conn:
            db_name = db_url.rsplit("/", 1)[-1]
            await conn.execute(sa.text(f'CREATE DATABASE "{db_name}"'))
    finally:
        await maint_engine.dispose()


@pytest_asyncio.fixture
async def engine():
    """Create a fresh test database for each test."""
    await _ensure_test_db(TEST_DATABASE_URL)
    eng = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def client(engine):
    test_session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_token(client, engine):
    """Create an admin user and return a valid auth token."""
    from src.auth.utils import hash_password
    from src.users.models import User

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db:
        admin = User(
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            first_name="Admin",
            last_name="User",
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        await db.commit()

    response = await client.post(
        "/api/v1/users/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )
    data = response.json()
    return data["access_token"]


@pytest_asyncio.fixture
async def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
