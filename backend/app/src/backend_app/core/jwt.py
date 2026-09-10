import datetime as dt
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, Response, status
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from backend_app.core.authenticate import Authenticate
from backend_app.database import AsyncSessionDep, db
from backend_app.models.user import UserModel


class Token:
    secret_key = db.settings.SECRET_JWT_KEY
    algorithm = "HS256"
    access_token_expire_minutes = 30

    class TokenData(BaseModel):
        username: str | None = None

    @staticmethod
    def create_access_token(
            data: dict,
            expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(dt.UTC) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Token.secret_key, Token.algorithm)
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        access_token: Annotated[str, Cookie()],
        session: AsyncSessionDep    
    ) -> UserModel :
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

        try:
            payload = jwt.decode(access_token, Token.secret_key, [Token.algorithm])
            username = payload.get("sub")

            if username is None :
                raise credentials_exception
            
            token_data = Token.TokenData(username=username)

        except InvalidTokenError:
            raise credentials_exception

        user = await Authenticate.get_user(token_data.username, session)

        if not user:
            raise credentials_exception

        return user

    @staticmethod
    def generate_token(
        email: str,
        response : Response
    ):
        access_token_expires = timedelta(minutes=Token.access_token_expire_minutes)
        access_token = Token.create_access_token(
            data={"sub": email},
            expires_delta=access_token_expires
        )
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=Token.access_token_expire_minutes*60,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax"
        )