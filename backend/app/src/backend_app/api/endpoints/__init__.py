from backend_app.api.endpoints.champions import router as champions_router
from backend_app.api.endpoints.stats import router as stats_router
from backend_app.api.endpoints.login import router as login_router
from backend_app.api.endpoints.signup import router as signup_router

__all__ = ["champions_router", "stats_router", "login_router", "signup_router"]