from typing import Annotated
import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update


from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserPublic
from shared.database import AsyncSessionDep
from backend_app.services.process_img import remove_file,

router = APIRouter()

@router.delete(
    "/remove_picture",
    response_model=UserPublic
)
async def remove_picture(
    session: AsyncSessionDep,
    current_user: Annotated[UserModel, Depends(Token.get_current_user)]
) -> UserModel:
    picture = current_user.picture

    if picture is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You don't have a profile picture to delete."
        )


    try:
        result = await session.execute(
            update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(picture=None)
            .returning(UserModel.id)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await session.commit()

    except Exception:
        await session.rollback()
        raise

    if not picture.startswith("https://cdn.intra.42.fr/users/"):
        path = os.path.join("/app/src/shared", picture)
        remove_file(path)

    await session.refresh(current_user)

    return current_user
    