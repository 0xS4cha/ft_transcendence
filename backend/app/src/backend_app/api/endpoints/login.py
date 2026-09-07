from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.database import AsyncSessionDep
from backend_app.models.user import UserModel
from backend_app.schemas.user import UserPublic

router = APIRouter()

@router.post("/token", response_model=Token.TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep
) -> Token.TokenResponse:
    user = await Password.authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=Token.access_token_expire_minutes)
    access_token = Token.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return Token.TokenResponse(access_token=access_token, token_type="bearer")

@router.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[UserModel, Depends(Token.get_current_user)]) -> UserModel:
    return current_user