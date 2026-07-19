from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.extensions.logs import get_logger


def register_error_handlers(app: FastAPI):
    from src.core import exceptions

    @app.exception_handler(exceptions.AppException)
    async def app_exception_handler(request: Request, exc: exceptions.AppException):
        logger = get_logger("app.errors")
        logger.warning(
            "app_exception",
            path=request.url.path,
            status=exc.status_code,
            code=exc.code,
            detail=exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "code": exc.code},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger = get_logger("app.errors")
        logger.exception("unhandled_exception", path=request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
