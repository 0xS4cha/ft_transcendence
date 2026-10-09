import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from backend_app.core.jwt import Token
from backend_app.core.websocket import WSbroadcast
from backend_app.models.friends import Friends, Status
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

logger = logging.getLogger(__name__)

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
        "/send_friend_request/{requested_username}",
        status_code=status.HTTP_201_CREATED
    )
async def send_friend_request(
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
    requested_username: str,
    session: AsyncSessionDep
) -> dict[str, Any]:
    requested = await session.scalar(
        select(UserModel)
        .where(UserModel.username == requested_username)
    )

    if requested is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The requested user with username {requested_username} does not exist."
        )

    if current_user.id == requested.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot send a friend request to yourself."
        )

    smallest_id = min(current_user.id, requested.id)
    largest_id = max(current_user.id, requested.id)

    try:
        result = await session.execute(
            insert(Friends)
            .values(
                requester=current_user.id,
                requested=requested.id,
                uid1=smallest_id,
                uid2=largest_id,
                status=Status.PENDING,
            )
            .on_conflict_do_nothing(constraint="uids")
            .returning(Friends.id)
        )
        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A friend request or friendship already exists."
            )
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        logger.warning(f"[send_friend_request] Integrity error while creating friend request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid friend request"
        ) from None

    try:
        await WSbroadcast("friend.request", {
            "requester_username": current_user.username
        }, [requested.id])
    except Exception as e: #noqa BLE001
        logger.warning(f"Failed to broadcast friend request to user with id {requested.id}: {e}")

    return {
        "message": "Friend request successfully sent."
    }