import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select

from backend_app.core.dependencies import RedisDep
from backend_app.core.jwt import Token
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserProfile
from shared.database import AsyncSessionDep

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/friends_list"
)
async def get_friends_list(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep,
    r: RedisDep,
) -> list[dict[str, str | int | bool | None]]:
    friendships = (await session.scalars(
        select(Friends)
        .where(
            or_(
                Friends.requested == current_user.id,
                Friends.requester == current_user.id
            )
        )
        .where(Friends.status == Status.ACCEPTED))
    ).all()

    if not friendships:
        return []

    ids = []
    for friendship in friendships:
        friend_id = friendship.requester if current_user.id == friendship.requested else friendship.requested
        ids.append(friend_id)

    friends = (await session.scalars(
        select(UserModel)
        .where(UserModel.id.in_(ids)))
        ).all()

    friends_by_id = {friend.id: friend for friend in friends}

    friends_list = []
    for friendship in friendships:
        friend_id = friendship.requester if current_user.id == friendship.requested else friendship.requested
        friend = friends_by_id.get(friend_id)
        if friend is None:
            logger.warning(f"[Friendship {friendship.id} references missing user {friend_id}")
            continue

        is_online = bool(await r.sismember("websocket:active_users", str(friend_id)))
        friends_list.append({**dict(UserProfile.model_validate(friend)), "online": is_online})

    return friends_list