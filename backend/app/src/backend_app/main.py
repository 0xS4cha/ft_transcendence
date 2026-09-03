from fastapi import FastAPI

from backend_app.api.router import api_router
from backend_app.database import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

@app.head("/health")
def health():
    return {"status": "healthy"}

@app.get("/")
def home():
    return {"message": "First FastAPI app"}
