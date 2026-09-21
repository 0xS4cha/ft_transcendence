from fastapi import APIRouter

from backend_app.api.endpoints import (
    accept_friend_request_router,
    champions_router,
    chat_router,
    items_data_router,
    login_router,
    login_with_42_router,
    logout_router,
    me_router,
    prometheus_metrics_router,
    refuse_friend_request_router,
    remove_friend_router,
    search_user_router,
    send_friend_request_router,
    signup_router,
    stats_router,
    websocket_router,
)

api_router = APIRouter(prefix="/api")

api_router.include_router(
    signup_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    me_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    login_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    login_with_42_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    logout_router,
    tags=["Authentication"],
    prefix="/auth"
)

api_router.include_router(
    champions_router,
    tags=["Champions"],
    prefix="/game_data/champions",
)

api_router.include_router(
    items_data_router,
    tags=["Items"],
    prefix="/game_data",
)

api_router.include_router(
    stats_router,
    tags=["Stats"],
    prefix="/stats",
)

api_router.include_router(
    prometheus_metrics_router,
    tags=["Prometheus Metrics"],
    prefix="/prometheus",
)

api_router.include_router(
	search_user_router,
	tags=["Seach User"],
	prefix="/search/user"
)

api_router.include_router(
	chat_router,
	tags=["Chat"],
	prefix="/chat"
)

api_router.include_router(
	websocket_router,
	tags=["WebSocket"],
	prefix="/websocket"
<<<<<<< HEAD
)
=======
)

api_router.include_router(
    send_friend_request_router,
    tags=["Friend"],
    prefix="/friends"
)

api_router.include_router(
    accept_friend_request_router,
    tags=["Friend"],
    prefix="/friends"
)

api_router.include_router(
    refuse_friend_request_router,
    tags=["Friend"],
    prefix="/friends"
)

api_router.include_router(
    friend_requests_list_router,
    tags=["Friend"],
    prefix="/friends"
)

api_router.include_router(
    friends_list_router,
    tags=["Friend"],
    prefix="/friends"
)

api_router.include_router(
    remove_friend_router,
    tags=["Friend"],
    prefix="/friends"
)
>>>>>>> main
