import datetime as dt
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, Response, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep, db


class Token:
    secret_key = db.settings.SECRET_JWT_KEY
    algorithm = "HS256"
    access_token_expire_minutes = 7 * 24 * 60

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        now = datetime.now(dt.UTC)
        to_encode = data.copy()
        to_encode.update({"iat": now, "exp": now + expires_delta})
        return jwt.encode(to_encode, Token.secret_key, algorithm=Token.algorithm)

    @staticmethod
    async def user_from_token(
        access_token: str | None,
        session: AsyncSession,
    ) -> UserModel | None:
        if not access_token:
            return None

        try:
            payload = jwt.decode(
                access_token,
                Token.secret_key,
                algorithms=[Token.algorithm],
                options={"require": ["exp", "sub"]},
            )
        except InvalidTokenError:
            return None

        sub = payload.get("sub")
        version = payload.get("ver")
        if not isinstance(sub, str) or not sub.isdigit() or not isinstance(version, int):
            return None

        user = await session.get(UserModel, int(sub))
        if user is None or user.token_version != version:
            return None

        return user

    @staticmethod
    async def get_current_user(
        session: AsyncSessionDep,
        access_token: Annotated[str | None, Cookie()] = None,
    ) -> UserModel:
        user = await Token.user_from_token(access_token, session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user

    @staticmethod
    def generate_token(user: UserModel, response: Response) -> None:
        access_token = Token.create_access_token(
            data={"sub": str(user.id), "ver": user.token_version},
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
