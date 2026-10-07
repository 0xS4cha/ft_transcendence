from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserPublic
from backend_app.core.jwt import Token
from shared.database import AsyncSessionDep
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post(
        "/change_username",
        response_model=UserPublic
)
async def change_username(
    new_username: str,
    session: AsyncSessionDep,
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
) -> UserModel:
    if new_username is current_user.username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You cannot use the same username as your current one."
        )
    
    result = await session.execute(
        update(UserModel)
        .where(UserModel.id == current_user.id)
        .values(username=new_username)
        .returning(UserModel.id)
    )

    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        )

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        )

    await session.refresh(current_user)

    return current_user