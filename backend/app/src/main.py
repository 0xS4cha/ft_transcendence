from fastapi import FastAPI
from .database import lifespan
from .routers.game_data.champions import router as champions_router
from .routers.stats import router as stats_router

app = FastAPI(lifespan=lifespan)
app.include_router(champions_router)
app.include_router(stats_router)


@app.head("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}