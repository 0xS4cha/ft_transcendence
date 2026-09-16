from typing import Annotated

from fastapi import APIRouter, Depends

from backend_app.core.jwt import Token
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserPublic

router = APIRouter()

@router.get("/me", response_model=UserPublic)
async def read_me(current_user: Annotated[UserModel, Depends(Token.get_current_user)]) -> UserModel:
    return current_user
