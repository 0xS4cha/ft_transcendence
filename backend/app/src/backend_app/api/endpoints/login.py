from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserPublic
from shared.database import AsyncSessionDep

router = APIRouter()

@router.post("/token", response_model=UserPublic)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep,
    response : Response
) -> dict[str, str]:
    user = await Password.authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    Token.generate_token(user.email, response)

    return user

@router.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[UserModel, Depends(Token.get_current_user)]) -> UserModel:
    return current_user