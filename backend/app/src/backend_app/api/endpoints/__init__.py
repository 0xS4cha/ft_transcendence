from backend_app.api.endpoints.authenticate import router as authenticate_router
from backend_app.api.endpoints.champions import router as champions_router
from backend_app.api.endpoints.stats import router as stats_router

__all__ = ["authenticate_router", "champions_router", "stats_router"]