from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import SHOW_DOCS_IN, settings
from src.db.engine import engine
from src.db.seed import run_migrations, seed_superuser
from src.extensions.error_handlers import register_error_handlers
from src.extensions.logs import configure_logging, get_logger
from src.extensions.middleware import log_requests
from src.router import register_routers


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


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
    if settings.ENVIRONMENT in SHOW_DOCS_IN
    else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_requests)
register_error_handlers(app)
register_routers(app)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
