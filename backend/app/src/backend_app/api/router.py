from fastapi import APIRouter

from backend_app.api.endpoints import (
    champions_router,
    login_router,
    prometheus_metrics_router,
    signup_router,
    stats_router,
	search_user_router
)

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

api_router.include_router(
    stats_router,
    tags=["Stats"],
    prefix="/stats",
)

api_router.include_router(
    prometheus_metrics_router,
    tags=["Prometheus Metrics"],
    prefix="/prometheus/metrics",
)

api_router.include_router(
	search_user_router,
	tags=["Seach User"],
	prefix="/search/user"
)
