from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select

from backend_app.core.jwt import Token
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.delete(
    "/remove_friend/{friend_username}"
)
async def remove_friend(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    session: AsyncSessionDep,
    friend_username: str
) -> dict[str, str]:
    friend = await session.scalar(
        select(UserModel)
        .where(UserModel.username == friend_username)
    )
    
    if friend is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {friend_username} does not exist."
        )

    if current_user.username == friend_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot remove yourself from your friends."
        )

    uid1 = min(current_user.id, friend.id)
    uid2 = max(current_user.id, friend.id)

    result = await session.execute(
        delete(Friends)
        .where(Friends.uid1 == uid1)
        .where(Friends.uid2 == uid2)
        .where(Friends.status == Status.ACCEPTED)
        .returning(Friends.id)
    )

    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with username {friend_username} is not your friend."
        )

    await session.commit()

    return {
        "message": "The friendship was successfully removed."
    }