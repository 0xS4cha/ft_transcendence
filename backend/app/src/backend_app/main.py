from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from backend_app.api.router import api_router
from backend_app.core.websocket import wsConnectionManager
from shared.database import db

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

print(f"\n\033[1;35mDATABASE_URL: \033[0;35m{db.settings.database_url}\033[0m\n")

app.include_router(api_router)

app.mount("/api/public", StaticFiles(directory="/app/src/shared/models_3d"), name="static")

@app.head("/health")
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def home():
    return {"message": "Tactyx FastAPI app"}
