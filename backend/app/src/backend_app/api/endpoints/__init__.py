from backend_app.api.endpoints.champions import router as champions_router
from backend_app.api.endpoints.items_data import router as items_data_router
from backend_app.api.endpoints.login import router as login_router
from backend_app.api.endpoints.logout import router as logout_router
from backend_app.api.endpoints.me import router as me_router
from backend_app.api.endpoints.oauth_login import router as login_with_42_router
from backend_app.api.endpoints.prometheus_metrics import (
    router as prometheus_metrics_router,
)
from backend_app.api.endpoints.search import router as search_user_router
from backend_app.api.endpoints.signup import router as signup_router
from backend_app.api.endpoints.stats import router as stats_router
from backend_app.api.endpoints.chat import router as chat_router
from backend_app.api.endpoints.websocket import router as websocket_router

__all__ = ["champions_router", "items_data_router", "login_router", "login_with_42_router", "logout_router", "me_router", "prometheus_metrics_router", "search_user_router", "signup_router", "stats_router", "chat_router", "websocket_router"]
