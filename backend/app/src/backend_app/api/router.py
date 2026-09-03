from fastapi import APIRouter

from backend_app.api.endpoints.authenticate import router as authenticate_router
from backend_app.api.endpoints.champions import router as champions_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    authenticate_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    champions_router,
    tags=["Game Data"],
    prefix="/champions"
)
