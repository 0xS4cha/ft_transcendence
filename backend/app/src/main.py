from fastapi import FastAPI
from .database import lifespan
from .routers.game_data.champions import router as champions_router

app = FastAPI(lifespan=lifespan)
app.include_router(champions_router)


@app.head("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}