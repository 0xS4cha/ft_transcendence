from datetime import datetime, timedelta
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from backend_app.core.authenticate import Authenticate
from backend_app.database import AsyncSessionDep, db
from backend_app.models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token:
    secret_key = db.settings.SECRET_JWT_KEY
    algoritm = "HS256"
    access_token_expire_minutes = 30

    class TokenResponse(BaseModel):
        access_token: str
        token_type: Literal["bearer"]

    class TokenData(BaseModel):
        username: str | None = None

    @staticmethod
    def create_access_token(
            data: dict,
            expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.now(datetime.UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Token.secret_key, Token.algoritm)
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSessionDep    
    ) -> UserModel :
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, Token.secret_key, [Token.algoritm])
            username = payload.get("sub")
            if username is None :
                raise credentials_exception
            token_data = Token.TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = await Authenticate.get_user(token_data.username, session )
        if not user:
            raise credentials_exception
        return user