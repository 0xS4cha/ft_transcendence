import datetime as dt
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, Response, status
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from backend_app.core.authenticate import Authenticate
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep, db


class Token:
    secret_key = db.settings.SECRET_JWT_KEY
    algorithm = "HS256"
    access_token_expire_minutes = 43200

    class TokenData(BaseModel):
        username: str | None = None

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        now = datetime.now(dt.UTC)
        to_encode = data.copy()
        to_encode.update({"iat": now, "exp": now + expires_delta})
        return jwt.encode(to_encode, Token.secret_key, algorithm=Token.algorithm)

    @staticmethod
    async def get_current_user(
        session: AsyncSessionDep,
        access_token: Annotated[str | None, Cookie()] = None,
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        if access_token is None:
            raise credentials_exception

        try:
            payload = jwt.decode(
                access_token,
                Token.secret_key,
                algorithms=[Token.algorithm],
                options={"require": ["exp", "sub"]},
            )
        except InvalidTokenError:
            raise credentials_exception

        token_data = Token.TokenData(username=payload.get("sub"))
        if token_data.username is None:
            raise credentials_exception

        user = await Authenticate.get_user(token_data.username, session)
        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    def generate_token(email: str, response: Response) -> None:
        access_token = Token.create_access_token(
            data={"sub": email.strip().lower()},
            expires_delta=timedelta(minutes=Token.access_token_expire_minutes),
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=Token.access_token_expire_minutes * 60,
            path="/",
            secure=db.settings.FRONTEND_URL.startswith("https"),
            httponly=True,
            samesite="lax",
        )