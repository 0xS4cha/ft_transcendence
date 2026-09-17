from typing import Any, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from backend_app.models.friends import Friends, Status
from shared.database import AsyncSessionDep

from sqlalchemy import select

router = APIRouter()

# @router.get(
#     "/friend_requests_list"
# )
# async def get_friend_requests_list(
#     current_user: Annotated[UserModel, Depends(Token.get_current_user)],
#     session: AsyncSessionDep
# ):
#     pending_requests = (await session.scalars(
#         select(Friends)
#         .where(Friends.)
#     )).all()