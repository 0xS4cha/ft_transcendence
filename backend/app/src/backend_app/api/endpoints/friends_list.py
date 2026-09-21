from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import or_, select

from backend_app.core.jwt import Token
from backend_app.core.model_to_dict import model_to_dict
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.get(
    "/friends_list"
)
async def get_friends_list(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    friends = (await session.scalars(
        select(Friends)
        .where(
            or_(
                Friends.requested == current_user.id,
                Friends.requester == current_user.id
            )
        )
        .where(Friends.status == Status.ACCEPTED))
    ).all()

    friend_ids= []
    for friend in friends:
        friend_id = friend.requester if current_user.id == friend.requested else friend.requested
        friend_ids.append(friend_id)

    friends_list = (await session.scalars(
        select(UserModel)
        .where(UserModel.id.in_(friend_ids)))
        ).all()

    friends_list_json = [model_to_dict(friend) for friend in friends_list]

    return friends_list_json