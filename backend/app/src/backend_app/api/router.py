from fastapi import APIRouter

from backend_app.api.endpoints import authenticate_router, champions_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    authenticate_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    champions_router,
    tags=["Champions"],
    prefix="/game_data/champions",
)
