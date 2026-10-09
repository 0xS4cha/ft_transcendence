from typing import Annotated

from fastapi import APIRouter, Cookie, Response
from sqlalchemy import update

from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.post("/logout")
async def logout(
    response: Response,
    session: AsyncSessionDep,
    access_token: Annotated[str | None, Cookie()] = None,
) -> None:
    user = await Token.user_from_token(access_token, session)
    if user is not None:
        await session.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(token_version=UserModel.token_version + 1)
        )
        await session.commit()

    response.delete_cookie(
        key="access_token",
        path="/"
    )
