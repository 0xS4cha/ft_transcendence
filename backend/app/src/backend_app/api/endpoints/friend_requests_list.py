from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserPublic
from shared.database import AsyncSessionDep

router = APIRouter()

@router.get(
    "/friend_requests_list"
)
async def get_friend_requests_list(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep
) -> list[UserPublic]:
    pending_requests = (await session.scalars(
        select(Friends)
        .where(Friends.requested == current_user.id)
        .where(Friends.status == Status.PENDING)
    )).all()

    if not pending_requests:
        return []


    ids = [request.requester for request in pending_requests]
    
    requesters = (await session.scalars(
        select(UserModel)
        .where(UserModel.id.in_(ids))
        )
    ).all()

    users_by_id = {user.id: user for user in requesters}

    requests_list = []
    for request in pending_requests:
        requester = users_by_id.get(request.requester)
        if requester is None:
            print(f"[Friend request {request.id} references missing user {request.requester}")
            continue
        requests_list.append(UserPublic.model_validate(requester))

    return requests_list