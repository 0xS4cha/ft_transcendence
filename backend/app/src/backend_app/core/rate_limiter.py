import time

import jwt
import redis.asyncio as redis
from fastapi import Depends, HTTPException, Request, WebSocket, status
from jwt.exceptions import InvalidTokenError

from backend_app.core.jwt import Token


async def hit(r: redis.Redis, key: str, times: int, seconds: int) -> bool:
    window = int(time.time()) // seconds
    redis_key = f"ratelimit:{key}:{seconds}:{window}"
    try:
        async with r.pipeline(transaction=True) as pipe:
            count, _ = await pipe.incr(redis_key).expire(redis_key, seconds).execute()
    except redis.RedisError as e:
        print(f"[rate_limiter] Redis unavailable, allowing request: {e}")
        return True
    return count <= times


class RateLimiter:
    def __init__(
        self,
        name: str,
        times: int,
        seconds: int,
        identifier
    ) -> None:
        self.name = name
        self.times = times
        self.seconds = seconds
        self.identifier = identifier

    async def __call__(
        self,
        request: Request,
    ) -> None:
        key = f"{self.name}:{await self.identifier(request)}"
        if not await hit(request.app.state.redis, key, self.times, self.seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too Many Requests",
                headers={"Retry-After": str(self.seconds)}
            )


def client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


async def ip_identifier(
    request: Request
) -> str:
    return f"ip:{client_ip(request)}"


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
            pass

    return f"ip:{client_ip(request)}"


def limit(name: str, times: int, seconds: int, identifier):
    return Depends(RateLimiter(name, times, seconds, identifier))

basic_limits = [limit("basic", 100, 60, ip_identifier)]
auth_limits = [limit("auth", 10, 60, ip_identifier)]
authenticated_limits = [
    limit("authenticated-user", 60, 60, user_identifier),
    limit("authenticated-ip", 200, 60, ip_identifier)
]


class WebSocketRateLimiter:
    def __init__(self, times: int, seconds: int) -> None:
        self.times = times
        self.seconds = seconds

    async def __call__(self, ws: WebSocket, context_key: str) -> bool:
        return await hit(ws.app.state.redis, f"ws:{context_key}", self.times, self.seconds)


ws_ratelimit = WebSocketRateLimiter(times=20, seconds=10)
