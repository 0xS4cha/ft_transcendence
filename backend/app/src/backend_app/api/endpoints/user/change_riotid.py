from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserPublic
from backend_app.core.jwt import Token
from shared.database import AsyncSessionDep
from sqlalchemy import update

router = APIRouter()

@router.post(
    "/change_riotid",
    response_model = UserPublic
)
async def change_riotid(
    new_riotid: str,
    session: AsyncSessionDep,
    current_user: Annotated[UserModel, Depends(Token.get_current_user)],
) -> UserModel:
    if new_riotid == current_user.riotid:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This is already your RiotID"
        )

    try:
        result = await session.execute(
            update(UserModel)
            .where(UserModel.id == current_user.id)
            .values(riotid=new_riotid)
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

    await session.refresh(current_user)
    
    return current_user