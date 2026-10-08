from backend_app.api.endpoints.auth.login import router as login_router
from backend_app.api.endpoints.auth.logout import router as logout_router
from backend_app.api.endpoints.auth.me import router as me_router
from backend_app.api.endpoints.auth.oauth_login import router as login_with_42_router
from backend_app.api.endpoints.auth.signup import router as signup_router
from backend_app.api.endpoints.chat.chat import router as chat_router
from backend_app.api.endpoints.chat.chatbot import router as chatbot_router
from backend_app.api.endpoints.chat.websocket import router as websocket_router
from backend_app.api.endpoints.friends.accept_friend_request import (
    router as accept_friend_request_router,
)
from backend_app.api.endpoints.friends.friend_requests_list import (
    router as friend_requests_list_router,
)
from backend_app.api.endpoints.friends.friends_list import router as friends_list_router
from backend_app.api.endpoints.friends.refuse_friend_request import (
    router as refuse_friend_request_router,
)
from backend_app.api.endpoints.friends.remove_friend import (
    router as remove_friend_router,
)
from backend_app.api.endpoints.friends.send_friend_request import (
    router as send_friend_request_router,
)
from backend_app.api.endpoints.game_data.augments_data import (
    router as augments_data_router,
)
from backend_app.api.endpoints.game_data.items_data import router as items_data_router
from backend_app.api.endpoints.game_data.leaderboard import router as leaderboard_router
from backend_app.api.endpoints.game_data.patchnote import router as patchnote_router
from backend_app.api.endpoints.game_data.search import router as search_router
from backend_app.api.endpoints.game_data.traits_data import router as traits_data_router
from backend_app.api.endpoints.game_data.units_data import router as units_data_router
from backend_app.api.endpoints.rgpd import router as rgpd_deletion_router
from backend_app.api.endpoints.stats.prometheus_metrics import (
    router as prometheus_metrics_router,
)
from backend_app.api.endpoints.stats.stats import router as stats_router
from backend_app.api.endpoints.user.change_picture import (
    router as change_picture_router,
)
from backend_app.api.endpoints.user.change_riotid import router as change_riotid_router
from backend_app.api.endpoints.user.change_username import (
    router as change_username_router,
)

__all__ = [
    "accept_friend_request_router",
    "augments_data_router",
    "change_picture_router",
    "change_riotid_router",
    "change_username_router",
    "chat_router",
    "chatbot_router",
    "friend_requests_list_router",
    "friends_list_router",
    "items_data_router",
    "leaderboard_router",
    "login_router",
    "login_with_42_router",
    "logout_router",
    "me_router",
    "patchnote_router",
    "prometheus_metrics_router",
    "refuse_friend_request_router",
    "remove_friend_router",
    "rgpd_deletion_router",
    "search_router",
    "send_friend_request_router",
    "signup_router",
    "stats_router",
    "traits_data_router",
    "units_data_router",
    "websocket_router"
]
