from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.core.model_to_dict import model_to_dict
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.get(
    "/friend_requests_list"
)
async def get_friend_requests_list(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep
) -> list[dict[str, Any]]:
    pending_requests = (await session.scalars(
        select(Friends)
        .where(Friends.requested == current_user.id)
        .where(Friends.status == Status.PENDING)
    )).all()

    to_serialize = [model_to_dict(request) for request in pending_requests]

    return to_serialize