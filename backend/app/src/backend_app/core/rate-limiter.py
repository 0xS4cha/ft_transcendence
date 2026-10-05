from fastapi import Request

from backend_app.core.jwt import Token
import jwt
from jwt.exceptions import InvalidTokenError

async def ip_identifier(
    request: Request
) -> str:
    return f"ip:{request.client.host}"

async def user_identifier(
    request: Request
) -> str:
    access_token = request.cookies.get("access_token")
    
    try:
        payload = jwt.decode(access_token, Token.secret_key, [Token.algorithm])
        username = payload.get("sub")

        if username:
            return f"user:{username}"
    except InvalidTokenError:
        print("[user_identifier] Invalid token.")

    return f"ip:{request.client.host}"