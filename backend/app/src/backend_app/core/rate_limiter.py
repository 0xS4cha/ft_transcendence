from fastapi import Depends, Request, WebSocket, HTTPException, status
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import WebSocketRateLimiter

from backend_app.core.jwt import Token
import jwt
from jwt.exceptions import InvalidTokenError


class RateLimiter:
    def __init__(
        self,
        limiter: Limiter,
        retry_after: int,
        identifier
    ) -> None:
        self.limiter = limiter
        self.identifier = identifier
        self.retry_after = retry_after

    async def __call__(
        self,
        request: Request,
    ) -> None:
        key = await self.identifier(request)
        ok = await self.limiter.try_acquire_async(key, blocking=False)
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too Many Requests",
                headers ={"Retry-After": str(self.retry_after)}
            )


async def ip_identifier(
    request: Request
) -> str:
    return f"ip:{request.client.host}"


async def user_identifier(
    request: Request
) -> str:
    access_token = request.cookies.get("access_token")

    if access_token:
        try:
            payload = jwt.decode(access_token, Token.secret_key, [Token.algorithm])
            username = payload.get("sub")

            if username:
                return f"user:{username}"
        except InvalidTokenError:
            print("[user_identifier] Invalid token.")

    return f"ip:{request.client.host}"


def limit(times: int, seconds: int, identifier):
    return Depends(RateLimiter(
        limiter=Limiter(Rate(times, Duration.SECOND * seconds)),
        retry_after=seconds,
        identifier=identifier,
    ))

basic_limits = [limit(100, 60, ip_identifier)]
auth_limits = [limit(10, 60, ip_identifier)]
authenticated_limits = [
    limit(60, 60, user_identifier),
    limit(200, 60, ip_identifier)
]

async def ws_identifier(ws: WebSocket) -> str:
    return f"ws:{ws.client.host}"


async def ws_callback(ws: WebSocket):
    await ws.close(code=1008, reason="Rate limit exceeded")


ws_ratelimit = WebSocketRateLimiter(
    limiter=Limiter(Rate(20, Duration.SECOND * 10)),
    identifier=ws_identifier,
    callback=ws_callback,
)