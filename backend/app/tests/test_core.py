"""Unit tests for pure helpers and infrastructure (no HTTP routes)."""

import asyncio
import json
from datetime import timedelta

import httpx
import jwt
import pytest
import redis.asyncio as redis
from fastapi import HTTPException
from starlette.testclient import TestClient

from backend_app.core import rate_limiter
from backend_app.core.jwt import Token
from backend_app.core.security import Password
from backend_app.core.utils import safe_get
from backend_app.core.websocket import WebsocketConnectionManager, wsConnectionManager
from backend_app.main import app
from backend_app.services.get_items import get_type
from backend_app.services.get_stats import get_all_datas_use, get_stats
from backend_app.services.get_traits import get_background_icon, get_breakpoints
from conftest import BASE_URL, REDIS_URL

# --- utils / stats ----------------------------------------------------------


@pytest.mark.parametrize("lst,idx,expected", [
    ([1, 2, 3], 0, 1), ([1, 2, 3], 2, 3), ([1, 2, 3], 3, None),
    ([1, 2, 3], -1, None), ([], 0, None),
])
def test_safe_get(lst, idx, expected):
    assert safe_get(lst, idx) == expected


def test_safe_get_default():
    assert safe_get([], 5, "d") == "d"


def test_get_stats():
    places = [10, 0, 0, 0, 0, 0, 0, 10]
    avg, winrate, freq = get_stats(places, 20, 40)
    assert avg == 4.5 and winrate == 50 and freq == 50


def test_get_stats_zero_total_usage():
    assert get_stats([1], 1, 0)[2] == 0


def test_get_stats_empty_places():
    """safe_get returns None on an empty list -> None / int TypeError."""
    with pytest.raises(ZeroDivisionError):
        get_stats([], 0, 0)


def test_get_all_datas_use():
    assert get_all_datas_use([{"places": [1, 2]}, {"places": [3]}]) == 6


def test_get_all_datas_use_missing_places():
    """A result without 'places' crashes the whole endpoint (sum(None))."""
    assert get_all_datas_use([{"places": [1]}, {}]) == 1


@pytest.mark.parametrize("name,expected", [
    ("TFT_Item_Rageblade", "Normal"), ("TFT_Item_BruiserEmblem", "Emblem"),
    ("TFT5_Item_RadiantRageblade", "Radiant"), ("TFT_Item_Artifact_X", "Artifact"),
])
def test_get_type(name, expected):
    assert get_type(name) == expected


def test_get_breakpoints():
    assert get_breakpoints({"effects": [{"minUnits": 2}, {"minUnits": None}]}) == ["2", "0"]
    assert get_breakpoints({}) is None
    assert get_breakpoints({"effects": [{}]}) is None


@pytest.mark.parametrize("bp,name,tid,expected", [
    ("0", "X", "a_1", "unique"), ("2", "X", "a_1", "bronze"), ("3", "X", "a_1", "silver"),
    ("11", "X", "a_1", "plat"), ("12", "X", "a_1", None), ("1", "Rival", "a_2", "bronze"),
])
def test_background_icon(bp, name, tid, expected):
    res = get_background_icon(tid, name, bp)
    assert (res is None) if expected is None else res.endswith(f"{expected}.png")


# --- security ---------------------------------------------------------------

def test_password_hash_roundtrip():
    h = Password.hash_password("hunter22!")
    assert h != "hunter22!" and h.startswith("$argon2")
    assert Password.verify_password("hunter22!", h)
    assert not Password.verify_password("hunter23!", h)


def test_token_roundtrip():
    tok = Token.create_access_token({"sub": "a@b.c"}, timedelta(minutes=1))
    payload = jwt.decode(tok, Token.secret_key, algorithms=["HS256"])
    assert payload["sub"] == "a@b.c" and "exp" in payload and "iat" in payload


def test_jwt_secret_is_strong():
    assert len(Token.secret_key) >= 32


# --- rate limiting ------------------------------------------------------------

async def _client_from(ip: str):
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, client=(ip, 1234)), base_url=BASE_URL
    )


async def test_auth_rate_limit_enforced():
    app.dependency_overrides.clear()
    async with await _client_from("10.9.9.1") as c:
        codes = [(await c.post("/api/auth/login", data={"username": "x@y.z", "password": "p"})).status_code
                 for _ in range(11)]
    assert codes[:10] == [401] * 10 and codes[10] == 429


async def test_rate_limit_is_per_ip():
    """pyrate_limiter's Limiter(Rate(...)) uses a SingleBucketFactory: the key is
    ignored and every client shares one bucket (10 logins/min for the whole site)."""
    app.dependency_overrides.clear()
    async with await _client_from("10.9.9.2") as c:
        for _ in range(10):
            await c.post("/api/auth/login", data={"username": "x@y.z", "password": "p"})
    async with await _client_from("10.9.9.3") as c:
        assert (await c.post("/api/auth/login", data={"username": "x@y.z", "password": "p"})).status_code == 401


async def test_rate_limit_shared_across_workers():
    """Two limiter instances (two workers / replicas) must share the same counters."""
    from starlette.requests import Request
    worker_a = rate_limiter.RateLimiter("shared", 3, 60, rate_limiter.ip_identifier)
    worker_b = rate_limiter.RateLimiter("shared", 3, 60, rate_limiter.ip_identifier)
    request = Request({"type": "http", "app": app, "client": ("10.9.9.4", 1), "headers": []})
    await worker_a(request)
    await worker_a(request)
    await worker_b(request)
    with pytest.raises(HTTPException) as exc:
        await worker_b(request)
    assert exc.value.status_code == 429


async def test_rate_limit_fails_open_when_redis_is_down(monkeypatch):
    broken = redis.from_url("redis://127.0.0.1:1", socket_connect_timeout=0.2)
    assert await rate_limiter.hit(broken, "k", 1, 60) is True
    await broken.aclose()


async def test_ws_rate_limit_is_per_user():
    class FakeWS:
        app = app
    for _ in range(20):
        assert await rate_limiter.ws_ratelimit(FakeWS(), context_key="1")
    assert not await rate_limiter.ws_ratelimit(FakeWS(), context_key="1")
    assert await rate_limiter.ws_ratelimit(FakeWS(), context_key="2")


async def test_auth_limit_covers_me_endpoint():
    """/auth/me is the only /auth route without auth_limits."""
    from backend_app.api import router as router_module
    me_routes = [r for r in router_module.api_router.routes if getattr(r, "path", "") == "/api/auth/me"]
    for r in me_routes:
        assert r.dependencies, f"{r.methods} /api/auth/me has no rate limit"


# --- websocket manager --------------------------------------------------------

class FakeWS:
    def __init__(self, fail=False):
        self.sent, self.fail = [], fail

    async def accept(self):
        pass

    async def send_json(self, msg):
        if self.fail:
            raise RuntimeError("socket closed")
        self.sent.append(msg)


async def wait_for(cond, timeout=2.0):
    for _ in range(int(timeout / 0.02)):
        if cond():
            return True
        await asyncio.sleep(0.02)
    return False


async def test_ws_broadcast_to_all_and_targeted():
    a, b = FakeWS(), FakeWS()
    await wsConnectionManager.connect(a, 1)
    await wsConnectionManager.connect(b, 2)
    try:
        await wsConnectionManager.broadcast({"t": "all"})
        await wsConnectionManager.broadcast({"t": "one"}, [2])
        assert await wait_for(lambda: len(b.sent) == 2)
        assert a.sent == [{"t": "all"}]
        assert await wsConnectionManager.redis.sismember(wsConnectionManager.ACTIVE_USERS_KEY, "1")
    finally:
        await wsConnectionManager.disconnect(a, 1)
        await wsConnectionManager.disconnect(b, 2)
    assert not await wsConnectionManager.redis.sismember(wsConnectionManager.ACTIVE_USERS_KEY, "1")


async def test_ws_user_stays_online_with_second_tab():
    a1, a2 = FakeWS(), FakeWS()
    await wsConnectionManager.connect(a1, 7)
    await wsConnectionManager.connect(a2, 7)
    await wsConnectionManager.disconnect(a1, 7)
    assert await wsConnectionManager.redis.sismember(wsConnectionManager.ACTIVE_USERS_KEY, "7")
    await wsConnectionManager.disconnect(a2, 7)


async def test_ws_dead_socket_is_dropped():
    dead = FakeWS(fail=True)
    await wsConnectionManager.connect(dead, 3)
    await wsConnectionManager.broadcast({"x": 1})
    assert await wait_for(lambda: (3, dead) not in wsConnectionManager.connections)


async def test_ws_listener_survives_malformed_message():
    """One bad payload on the pub/sub channel kills the listener task for good:
    every later broadcast is silently dropped until the process restarts."""
    mgr = WebsocketConnectionManager(REDIS_URL)
    mgr.REDIS_CHANNEL = "audit:isolated-channel"  # keep the app's own listener out of it
    await mgr.start()
    ws = FakeWS()
    await mgr.connect(ws, 5)
    try:
        await asyncio.sleep(0.1)
        await mgr.redis.publish(mgr.REDIS_CHANNEL, "not json")
        await asyncio.sleep(0.1)
        await mgr.broadcast({"after": True})
        assert await wait_for(lambda: ws.sent == [{"after": True}])
    finally:
        await mgr.disconnect(ws, 5)
        await mgr.stop()


async def test_ws_listener_survives_redis_restart():
    """No reconnect logic: if Redis drops the pub/sub connection the listener dies."""
    mgr = WebsocketConnectionManager(REDIS_URL)
    mgr.redis = redis.from_url(REDIS_URL, decode_responses=True, client_name="audit-pubsub")
    mgr.REDIS_CHANNEL = "audit:isolated-channel-2"
    await mgr.start()
    await asyncio.sleep(0.1)
    try:
        clients = await mgr.redis.client_list()
        for c in clients:
            if c.get("name") == "audit-pubsub" and int(c.get("sub", 0)) > 0:
                await mgr.redis.client_kill_filter(_id=c["id"])
        await asyncio.sleep(0.3)
        assert not mgr._listener_task.done()
    finally:
        await mgr.stop()


def test_ws_endpoint_rejects_unauthenticated():
    tc = TestClient(app, base_url=BASE_URL)  # no `with`: don't run the app lifespan again
    from starlette.websockets import WebSocketDisconnect
    if True:
        with pytest.raises(WebSocketDisconnect) as exc, tc.websocket_connect("/api/websocket/ws") as ws:
            ws.receive_text()
        assert exc.value.code == 1008


def test_json_default_handles_datetimes():
    import datetime
    out = json.dumps({"d": datetime.date(2026, 1, 2)}, default=WebsocketConnectionManager._json_default)
    assert "2026-01-02" in out
