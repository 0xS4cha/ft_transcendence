from backend_app.api.endpoints.accept_friend_request import (
    router as accept_friend_request_router,
)
from backend_app.api.endpoints.champions import router as champions_router
from backend_app.api.endpoints.chat import router as chat_router
from backend_app.api.endpoints.friend_requests_list import (
    router as friend_requests_list_router,
)
from backend_app.api.endpoints.friends_list import router as friends_list_router
from backend_app.api.endpoints.items_data import router as items_data_router
from backend_app.api.endpoints.leaderboard import router as leaderboard_router
from backend_app.api.endpoints.login import router as login_router
from backend_app.api.endpoints.logout import router as logout_router
from backend_app.api.endpoints.me import router as me_router
from backend_app.api.endpoints.oauth_login import router as login_with_42_router
from backend_app.api.endpoints.prometheus_metrics import (
    router as prometheus_metrics_router,
)
from backend_app.api.endpoints.refuse_friend_request import (
    router as refuse_friend_request_router,
)
from backend_app.api.endpoints.remove_friend import router as remove_friend_router
from backend_app.api.endpoints.search import router as search_user_router
from backend_app.api.endpoints.send_friend_request import (
    router as send_friend_request_router,
)
from backend_app.api.endpoints.signup import router as signup_router
from backend_app.api.endpoints.stats import router as stats_router
from backend_app.api.endpoints.traits_data import router as traits_data_router
from backend_app.api.endpoints.units_data import router as units_data_router
from backend_app.api.endpoints.websocket import router as websocket_router

__all__ = ["accept_friend_request_router",
           "champions_router",
           "chat_router",
           "friend_requests_list_router",
           "friends_list_router",
           "items_data_router",
           "leaderboard_router",
           "login_router",
           "login_with_42_router",
           "logout_router",
           "me_router",
           "prometheus_metrics_router",
           "refuse_friend_request_router",
           "remove_friend_router",
           "search_user_router",
           "send_friend_request_router",
           "signup_router",
           "stats_router",
           "traits_data_router",
           "units_data_router",
           "websocket_router",
]
