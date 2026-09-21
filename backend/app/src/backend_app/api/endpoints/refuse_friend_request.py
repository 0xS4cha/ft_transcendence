from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.models.friends import Friends, Status
from shared.database import AsyncSessionDep
from sqlalchemy import select

router = APIRouter()

@router.delete(
    "/refuse_friend_request/{friend_request_id}"
)
async def refuse_friend_request(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    friend_request_id: int,
    session: AsyncSessionDep
) -> dict[str, str]:
    existing_request = await session.scalar(
        select(Friends)
        .where(Friends.id == friend_request_id)
    )

    if existing_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The friend request does not exist."
        )

    if current_user.id != existing_request.requested:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the requested user."
        )
    
    if existing_request.status != Status.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user is already your friend."
        )

    await session.delete(existing_request)
    await session.commit()
    
    return {
        "message": "Friend request successfully refused."
    }