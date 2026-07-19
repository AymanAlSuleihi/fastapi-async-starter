from contextlib import asynccontextmanager

from src.core.config import settings
from src.db.engine import engine
from src.db.seed import run_migrations, seed_superuser
from src.extensions.logs import configure_logging, get_logger


@asynccontextmanager
async def lifespan(app):
    configure_logging()
    logger = get_logger("app.lifespan")
    logger.info("starting_up", environment=settings.ENVIRONMENT)
    try:
        await run_migrations()
        logger.info("migrations_complete")
        await seed_superuser()
        logger.info("seeding_complete")
    except Exception:
        logger.exception("startup_failed")
        raise
    yield
    logger.info("shutting_down")
    await engine.dispose()
