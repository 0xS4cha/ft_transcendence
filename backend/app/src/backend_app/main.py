from contextlib import asynccontextmanager

from fastapi import FastAPI

import backend_app.models  # noqa: F401
from backend_app.api.router import api_router
from shared.database import db
from backend_app.core.websocket import wsConnectionManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await wsConnectionManager.start()

    try:
        async with db.lifespan(app):
            yield
    finally:
        await wsConnectionManager.stop()

app = FastAPI(lifespan=lifespan)

print(f"\n\033[1;35mDATABASE_URL: \033[0;35m{db.settings.database_url}\033[0m\n")

app.include_router(api_router)

@app.head("/health")
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def home():
    return {"message": "First FastAPI app"}
