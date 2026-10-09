"""Property-based fuzzing: random path params, query strings, bodies and cookies
must never produce a 5xx. Upstream services stay blocked (network down), so
these tests also check that every endpoint degrades gracefully offline.
"""

from urllib.parse import quote

import httpx
import pytest
from conftest import BASE_URL
from hypothesis import HealthCheck, example, given, settings
from hypothesis import strategies as st

from backend_app.main import app

FUZZ = settings(
    max_examples=150,
    deadline=None,
    suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)

# Printable-ish text that is still valid inside a URL once percent-encoded.
text = st.text(st.characters(blacklist_categories=["Cs"]), max_size=200)
segment = text.filter(lambda s: s not in ("", ".", "..") and "/" not in s)


async def call(method, url, cookie=None, **kw):
    headers = {"Cookie": f"access_token={cookie}"} if cookie is not None else {}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, raise_app_exceptions=False),
        base_url=BASE_URL,
    ) as c:
        return await c.request(method, url, headers=headers, **kw)


def assert_no_5xx(resp, ctx):
    graceful = (502, 503)
    assert resp.status_code < 500 or resp.status_code in graceful, (
        f"{resp.status_code} for {ctx}: {resp.text[:300]}"
    )


async def logged_in_cookie():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as c:
        await c.post("/api/auth/signup", json={
            "email": "fuzz@example.com", "username": "fuzzer",
            "password": "Password123!", "confirm_password": "Password123!",
        })
        r = await c.post("/api/auth/login", data={"username": "fuzz@example.com", "password": "Password123!"})
        return r.cookies.get("access_token")


# --- unauthenticated endpoints -------------------------------------------

@FUZZ
@given(q=segment)
async def test_fuzz_search(q):
    assert_no_5xx(await call("GET", f"/api/search/{quote(q, safe="")}"), q)


@FUZZ
@given(server=text)
@example(server="BR1")
async def test_fuzz_leaderboard(server):
    assert_no_5xx(await call("GET", "/api/leaderboard/", params={"server": server}), server)


@FUZZ
@given(lang=text)
async def test_fuzz_patchnote(lang):
    assert_no_5xx(await call("GET", "/api/patchnote/latest", params={"lang": lang}), lang)


@FUZZ
@given(endpoint=st.sampled_from(["items_data", "traits_data", "units_data"]),
       queue=text, rank=text, server=text)
async def test_fuzz_game_data_filters(endpoint, queue, rank, server):
    resp = await call("GET", f"/api/game_data/{endpoint}",
                      params={"queue": queue, "rank": rank, "server": server})
    assert_no_5xx(resp, (endpoint, queue, rank, server))


@FUZZ
@given(name=segment)
@example(name="home")
async def test_fuzz_stats(name):
    assert_no_5xx(await call("GET", f"/api/stats/{quote(name, safe="")}"), name)


@FUZZ
@given(body=st.one_of(
    st.dictionaries(st.sampled_from(["email", "username", "password", "confirm_password"]),
                    st.one_of(text, st.integers(), st.none(), st.lists(text, max_size=2))),
    st.lists(st.integers(), max_size=3), text, st.none(),
))
async def test_fuzz_signup(body):
    assert_no_5xx(await call("POST", "/api/auth/signup", json=body), body)


@FUZZ
@given(username=text, password=text)
@example(username="\x00", password="x")
async def test_fuzz_login(username, password):
    resp = await call("POST", "/api/auth/login", data={"username": username, "password": password})
    assert_no_5xx(resp, (username, password))


@FUZZ
@given(code=st.one_of(st.none(), text), state=st.one_of(st.none(), text), saved=st.one_of(st.none(), text))
@example(code="c", state="s", saved="s")
async def test_fuzz_oauth_callback(code, state, saved):
    params = {k: v for k, v in {"code": code, "state": state}.items() if v is not None}
    headers = {"Cookie": f"oauth_state={saved}"} if saved and saved.isascii() and saved.isprintable() and ";" not in saved else {}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app, raise_app_exceptions=False), base_url=BASE_URL
    ) as c:
        resp = await c.get("/api/auth/login_with_42/callback", params=params, headers=headers)
    assert_no_5xx(resp, (code, state, saved))


# --- authentication token -------------------------------------------------

jwt_like = st.one_of(
    st.text(st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.=!+/"), max_size=300),
    st.builds(lambda a, b, c: f"{a}.{b}.{c}",
              st.sampled_from(["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9", "eyJhbGciOiJub25lIn0", "e30", "", "!!"]),
              st.text(st.sampled_from("abcXYZ019-_=!"), max_size=50),
              st.text(st.sampled_from("abcXYZ019-_=!"), max_size=50)),
)


@FUZZ
@given(token=jwt_like, path=st.sampled_from([
    "/api/auth/me", "/api/friends/friends_list", "/api/chat/messages", "/api/friends/friend_requests_list",
]))
async def test_fuzz_auth_cookie(token, path):
    resp = await call("GET", path, cookie=token)
    assert_no_5xx(resp, token)
    assert resp.status_code == 401


# --- authenticated endpoints ----------------------------------------------

@pytest.fixture
async def cookie():
    return await logged_in_cookie()


@FUZZ
@given(name=segment, action=st.sampled_from([
    ("POST", "send_friend_request"), ("POST", "accept_friend_request"),
    ("DELETE", "refuse_friend_request"), ("DELETE", "remove_friend"),
]))
@example(name="\x00", action=("POST", "send_friend_request"))
async def test_fuzz_friend_endpoints(cookie, name, action):
    method, ep = action
    resp = await call(method, f"/api/friends/{ep}/{quote(name, safe="")}", cookie=cookie)
    assert_no_5xx(resp, (ep, name))


@FUZZ
@given(new=text)
@example(new="\x00")
async def test_fuzz_change_username(cookie, new):
    resp = await call("POST", "/api/user/change_username", cookie=cookie, params={"new_username": new})
    assert_no_5xx(resp, new)


@FUZZ
@given(content=st.one_of(text, st.none(), st.integers()))
@example(content="hello")
async def test_fuzz_chat_send(cookie, content):
    resp = await call("POST", "/api/chat/send", cookie=cookie, json={"content": content})
    assert_no_5xx(resp, content)


@FUZZ
@given(data=st.binary(max_size=4096))
async def test_fuzz_change_picture(cookie, data):
    resp = await call("POST", "/api/user/change_picture", cookie=cookie,
                      files={"file": ("x.png", data, "image/png")})
    assert_no_5xx(resp, data[:20])


@FUZZ
@given(message=text)
async def test_fuzz_chatbot(cookie, message):
    from backend_app.api.endpoints.chat import chatbot as mod

    async def fake_chat(**_kw):
        return {"message": {"content": "ok"}}
    original = mod.chatbot.client.chat
    mod.chatbot.client.chat = fake_chat
    try:
        resp = await call("GET", "/api/chatbot/ask", cookie=cookie, params={"message": message})
    finally:
        mod.chatbot.client.chat = original
    assert_no_5xx(resp, message)
