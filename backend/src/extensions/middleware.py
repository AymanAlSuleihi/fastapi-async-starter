import time

from fastapi import Request

from src.extensions.logs import get_logger


async def log_requests(request: Request, call_next):
    logger = get_logger("app.http")
    start = time.monotonic()
    response = await call_next(request)
    duration_ms = (time.monotonic() - start) * 1000
    if request.url.path != "/health":
        logger.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
    return response
