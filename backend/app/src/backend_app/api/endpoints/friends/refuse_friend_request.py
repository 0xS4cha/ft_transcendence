from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, delete, or_, select

from backend_app.core.jwt import Token
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.delete(
    "/refuse_friend_request/{requester_username}"
)
async def refuse_friend_request(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    requester_username: str,
    session: AsyncSessionDep
) -> dict[str, str]:
    requester = await session.scalar(
        select(UserModel)
        .where(UserModel.username == requester_username)
    )
    
    if requester is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The requester with username {requester_username} does not exist."
        )

    if current_user.username == requester_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot refuse a friend request from yourself."
        )
    
    result = await session.execute(
        delete(Friends)
        .where(
            or_(
                and_(Friends.requested == current_user.id, Friends.requester == requester.id),
                and_(Friends.requester == current_user.id, Friends.requested == requester.id),
            )
        )
        .where(Friends.status == Status.PENDING)
        .returning(Friends.id)
    )

    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The friend request does not exist."
        )
    
    await session.commit()
    
    return {
        "message": "Friend request successfully refused."
    }