from backend_app.api.endpoints.champions import router as champions_router
from backend_app.api.endpoints.login import router as login_router
from backend_app.api.endpoints.logout import router as logout_router
from backend_app.api.endpoints.prometheus_metrics import (
    router as prometheus_metrics_router,
)
from backend_app.api.endpoints.search import router as search_user_router
from backend_app.api.endpoints.signup import router as signup_router
from backend_app.api.endpoints.stats import router as stats_router

__all__ = ["champions_router", "login_router", "logout_router", "prometheus_metrics_router", "search_user_router", "signup_router", "stats_router"]
