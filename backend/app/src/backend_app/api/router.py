from fastapi import APIRouter

from backend_app.api.endpoints import champions_router, login_router, signup_router

api_router = APIRouter(prefix="/api")

api_router.include_router(
    signup_router,
    tags=["Authentication"],
    prefix="/auth/signup"
)

api_router.include_router(
    login_router,
    tags=["Authentication"],
    prefix="/auth/login"
)

api_router.include_router(
    champions_router,
    tags=["Champions"],
    prefix="/game_data/champions",
)
