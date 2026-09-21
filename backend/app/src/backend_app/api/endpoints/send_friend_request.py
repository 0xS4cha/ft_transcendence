from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()
    
def create_friend_request(
    requester_id: int,
    requested_id: int,
) -> Friends:
    friend_request = Friends(
        requester=requester_id,
        requested=requested_id,
        uid1=requester_id,
        uid2=requested_id,
        status=Status.PENDING,
    )

    return friend_request

@router.post(
        "/send_friend_request/{requested_id}",
        status_code=status.HTTP_201_CREATED
    )
async def send_friend_request(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    requested_id: int,
    session: AsyncSessionDep
) -> dict[str, Any]:
    requested_user = await session.scalar(
        select(UserModel)
        .where(UserModel.id == requested_id)
    )

    if requested_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested user does not exist."
        )
    
    requester_id = current_user.id;

    if requester_id == requested_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot send a friend request to yourself."
        )

    smallest_id = min(requester_id, requested_id)
    largest_id = max(requester_id, requested_id)

    existing_request = await session.scalar(
        select(Friends)
        .where(Friends.uid1 == smallest_id)
        .where(Friends.uid2 == largest_id)
    )

    if existing_request:
        if existing_request.status == Status.PENDING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A friend request is already pending."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{requested_user.username} is already your friend."
            )

    friend_request = create_friend_request(requester_id, requested_id)

    session.add(friend_request)
    await session.commit()
    await session.refresh(friend_request)

    return {
        "message": "Friend request successfully sent."
    }