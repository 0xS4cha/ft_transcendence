"""Shared fixtures for the backend test suite.

The suite expects the same environment as the backend container: a Postgres
reachable as `postgres`, a Redis reachable as `redis`, and the paths under
/app/src. See tests/README.md for how to run it in a throwaway container.

Every test starts from empty tables, an empty Redis and cleared module caches.
All outbound HTTP is blocked by default; tests that need an upstream response
patch the specific function they exercise.
"""

import io
import itertools
from collections.abc import AsyncIterator, Awaitable, Callable

import aiohttp
import httpx
import httpx2
import pytest
import redis.asyncio as redis
import requests
from PIL import Image
from sqlalchemy import text

from backend_app.api.endpoints.chat import chat as chat_module
from backend_app.api.endpoints.game_data import leaderboard as leaderboard_module
from backend_app.api.endpoints.game_data import patchnote as patchnote_module
from backend_app.api.endpoints.stats import stats as stats_module
from backend_app.core import rate_limiter
from backend_app.core.websocket import wsConnectionManager
from backend_app.main import app
from shared.database import db

BASE_URL = "https://testserver"
REDIS_URL = "redis://redis:6379"

ALL_LIMITERS = [
    *rate_limiter.basic_limits,
    *rate_limiter.auth_limits,
    *rate_limiter.authenticated_limits,
]


def _blocked(exc_type):
    """Simulate 'network unreachable' with the exception each client really raises."""
    def raiser(*_args, **_kwargs):
        raise exc_type("network blocked in tests")
    return raiser


@pytest.fixture(scope="session", autouse=True)
async def app_state() -> AsyncIterator[None]:
    app.state.redis = redis.from_url(REDIS_URL, decode_responses=True)
    await wsConnectionManager.start()
    yield
    await wsConnectionManager.stop()
    await app.state.redis.aclose()
    await db.engine.dispose()


@pytest.fixture(autouse=True)
async def clean_state() -> AsyncIterator[None]:
    async with db.engine.begin() as conn:
        await conn.execute(text(
            "TRUNCATE chat_message, friends, users, visit_model "
            "RESTART IDENTITY CASCADE"
        ))
    await app.state.redis.flushdb()

    chat_module.cached_messages = []
    chat_module.last_refresh_timestamp = 0
    leaderboard_module.cache.clear()
    leaderboard_module.last_calculated_timestamp = 0
    patchnote_module.cached_patchnote.clear()
    stats_module.stats_cache.clear()
    stats_module.tft_stats.clear()
    for endpoint in stats_module.endpoints.values():
        endpoint["last"] = 0.0
    yield


@pytest.fixture(autouse=True)
def no_rate_limits() -> AsyncIterator[None]:
    """Rate limiting is covered by its own tests; disable it everywhere else."""
    async def allow() -> None:
        return None

    for dep in ALL_LIMITERS:
        app.dependency_overrides[dep.dependency] = allow
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(httpx2.AsyncClient, "send", _blocked(httpx2.ConnectError))
    # Only the real network transport: the test client itself uses ASGITransport.
    monkeypatch.setattr(httpx.AsyncHTTPTransport, "handle_async_request", _blocked(httpx.ConnectError))
    monkeypatch.setattr(requests, "post", _blocked(requests.ConnectionError))
    monkeypatch.setattr(requests, "get", _blocked(requests.ConnectionError))
    monkeypatch.setattr("aiohttp.ClientSession._request", _blocked(aiohttp.ClientConnectionError))


@pytest.fixture
async def client() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as c:
        yield c


_counter = itertools.count()


@pytest.fixture
async def make_user() -> AsyncIterator[Callable[..., Awaitable[httpx.AsyncClient]]]:
    """Factory returning a logged-in client for a freshly signed-up user."""
    clients: list[httpx.AsyncClient] = []

    async def factory(username: str | None = None, password: str = "Password123!"):
        n = next(_counter)
        username = username or f"user{n}"
        c = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url=BASE_URL
        )
        clients.append(c)
        resp = await c.post("/api/auth/signup", json={
            "email": f"{username}@example.com",
            "username": username,
            "password": password,
            "confirm_password": password,
        })
        assert resp.status_code == 200, resp.text
        c.user = resp.json()  # type: ignore[attr-defined]
        return c

    yield factory
    for c in clients:
        await c.aclose()


def image_bytes(fmt: str = "PNG", size: tuple[int, int] = (64, 64), mode: str = "RGB") -> bytes:
    buf = io.BytesIO()
    Image.new(mode, size, color=(200, 30, 30) if mode == "RGB" else None).save(buf, format=fmt)
    return buf.getvalue()
