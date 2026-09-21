from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.models.friends import Friends, Status
from shared.database import AsyncSessionDep

from sqlalchemy import select

router = APIRouter()

@router.delete(
    "/remove_friend/{friend_request_id}"
)
async def remove_friend(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep,
    friend_request_id: int
) -> dict[str, str]:
    existing_friendship = await session.scalar(
        select(Friends)
        .where(Friends.id == friend_request_id)
    )

    if existing_friendship is None or existing_friendship.status != Status.ACCEPTED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The friendship does not exist."
        )

    if current_user.id != existing_friendship.requested and current_user.id != existing_friendship.requester:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The friendship is not yours."
        )
    
    await session.delete(existing_friendship)
    await session.commit()

    return {
        "message": "The friendship was successfully removed."
    }