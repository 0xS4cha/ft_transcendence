from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from backend_app.core.authenticate import Authenticate
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.schemas.user import USERNAME_PATTERN, UserPublic
from shared.database import AsyncSessionDep

router = APIRouter()

@router.post(
        "/change_username",
        response_model=UserPublic
)
async def change_username(
    new_username: Annotated[str, Query(pattern=USERNAME_PATTERN)],
    session: AsyncSessionDep,
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
) -> UserModel:
    if new_username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You cannot use the same username as your current one."
        )

    if await Authenticate.username_taken(new_username, session, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        )

    try:
        result = await session.execute(
            update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(username=new_username)
            .returning(UserModel.id)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        ) from None

    await session.refresh(current_user)

    return current_user