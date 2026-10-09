from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.models.users import UserModel
from backend_app.schemas.user import UserPublic
from shared.database import AsyncSessionDep

router = APIRouter()


@router.post("/login", response_model=UserPublic)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionDep,
    response: Response,
) -> UserModel:
    user = await Password.authenticate_user(
        form_data.username.strip().lower(), form_data.password, session
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    Token.generate_token(user.email, response)
    return user