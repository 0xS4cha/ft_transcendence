import logging
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as redis
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import DataError, DBAPIError

from backend_app.api.router import api_router
from backend_app.core.websocket import wsConnectionManager
from shared.database import db

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await wsConnectionManager.start()
    app.state.redis = redis.from_url("redis://redis:6379", decode_responses=True)
    
    try:
        async with db.lifespan(app):
            yield

    finally:
        await app.state.redis.aclose()
        await wsConnectionManager.stop()

app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs" if db.settings.DEBUG else None,
    redoc_url="/redoc" if db.settings.DEBUG else None,
    openapi_url="/openapi.json" if db.settings.DEBUG else None
)

app.include_router(api_router)


def is_invalid_input(exc: DBAPIError) -> bool:
    if isinstance(exc, DataError):
        return True
    cause = exc.orig.__cause__ if exc.orig is not None else None
    return isinstance(cause, asyncpg.exceptions.DataError)


@app.exception_handler(DBAPIError)
async def invalid_data_handler(_request: Request, exc: DBAPIError) -> JSONResponse:
    if not is_invalid_input(exc):
        raise exc
    logger.warning(f"[invalid_data_handler] {exc.orig!r}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid input"},
    )

app.mount("/api/public/models_3d", StaticFiles(directory="/app/src/shared/models_3d"), name="models_3d")
app.mount("/api/public/profile_pictures", StaticFiles(directory="/app/src/shared/profile_pictures"), name="profile_pictures")


@app.exception_handler(asyncpg.exceptions.CharacterNotInRepertoireError)
async def character_not_in_repertoire_handler(
    request: Request,
    exc: asyncpg.exceptions.CharacterNotInRepertoireError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Input contains an unsupported character."
        },
    )

@app.exception_handler(DBAPIError)
async def sqlalchemy_db_error_handler(
    request: Request,
    exc: DBAPIError,
):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input data."},
    )

@app.exception_handler(asyncpg.exceptions.DataError)
async def data_error_handler(
    request: Request,
    exc: asyncpg.exceptions.DataError,
):
    print(exc)
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid input data."
        },
    )


@app.head("/health")
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def home():
    return {"message": "Tactyx FastAPI app"}
