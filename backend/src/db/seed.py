import asyncio
import os
from pathlib import Path

from alembic.config import Config
from sqlalchemy import select

from alembic import command
from src.auth.utils import hash_password
from src.core.config import settings
from src.db.engine import SessionFactory
from src.users.models import User


def _get_alembic_cfg() -> Config:
    ini_path = Path(__file__).resolve().parent.parent / "alembic.ini"
    cfg = Config(str(ini_path))
    db_url = os.getenv("DATABASE_URL", "")
    if db_url:
        cfg.set_main_option("sqlalchemy.url", db_url)
    return cfg


async def run_migrations() -> None:
    """Apply any pending Alembic migrations."""
    cfg = _get_alembic_cfg()
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, command.upgrade, cfg, "head")


async def seed_superuser() -> None:
    """Create the initial admin user if one doesn't already exist."""
    async with SessionFactory() as db:
        existing = await db.scalar(select(User).where(User.email == settings.SUPERUSER_EMAIL))
        if not existing:
            admin = User(
                email=settings.SUPERUSER_EMAIL,
                hashed_password=hash_password(settings.SUPERUSER_PASSWORD),
                first_name="Admin",
                last_name="User",
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            await db.commit()
