from datetime import UTC, datetime, timedelta

import jwt
import pytest
from sqlalchemy import select, update

from backend_app.api.endpoints.auth import oauth_login
from backend_app.core.jwt import Token
from backend_app.models.users import UserModel
from shared.database import db

SIGNUP = {
    "email": "alice@example.com",
    "username": "alice",
    "password": "Password123!",
    "confirm_password": "Password123!",
}


# --- signup ---------------------------------------------------------------

async def test_signup_creates_user_and_sets_cookie(client):
    resp = await client.post("/api/auth/signup", json=SIGNUP)
    assert resp.status_code == 200
    body = resp.json()
    assert body["username"] == "alice"
    assert "hashed_password" not in body
    assert "access_token" in resp.cookies
    cookie = resp.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=lax" in cookie and "secure" in cookie


async def test_signup_normalizes_email(client):
    resp = await client.post("/api/auth/signup", json={**SIGNUP, "email": "  ALICE@Example.COM "})
    assert resp.status_code == 200
    assert resp.json()["email"] == "alice@example.com"


async def test_signup_duplicate_email_case_insensitive(client):
    await client.post("/api/auth/signup", json=SIGNUP)
    resp = await client.post("/api/auth/signup", json={
        **SIGNUP, "email": "Alice@Example.com", "username": "other"
    })
    assert resp.status_code == 409


async def test_signup_duplicate_username(client):
    await client.post("/api/auth/signup", json=SIGNUP)
    resp = await client.post("/api/auth/signup", json={**SIGNUP, "email": "b@example.com"})
    assert resp.status_code == 409


async def test_signup_username_differs_only_by_case_is_rejected(client):
    """'Alice' and 'alice' would look identical in chat and friend lists."""
    await client.post("/api/auth/signup", json=SIGNUP)
    resp = await client.post("/api/auth/signup", json={
        **SIGNUP, "email": "b@example.com", "username": "Alice"
    })
    assert resp.status_code == 409


@pytest.mark.parametrize("override", [
    {"confirm_password": "different1"},
    {"password": "short", "confirm_password": "short"},
    {"password": "x" * 129, "confirm_password": "x" * 129},
    {"email": "not-an-email"},
    {"username": "ab"},
    {"username": "a" * 33},
])
async def test_signup_validation_errors(client, override):
    resp = await client.post("/api/auth/signup", json={**SIGNUP, **override})
    assert resp.status_code == 422


@pytest.mark.parametrize("username", [
    "../../etc", "a/b", "with space", "<script>x</script>", "   ", "abc\n",
])
async def test_signup_rejects_unsafe_usernames(client, username):
    """Usernames are used in URL paths (/friends/.../{username}) and rendered in the UI."""
    resp = await client.post("/api/auth/signup", json={**SIGNUP, "username": username})
    assert resp.status_code == 422


async def test_signup_missing_body(client):
    resp = await client.post("/api/auth/signup")
    assert resp.status_code == 422


# --- login ----------------------------------------------------------------

async def test_login_success(client):
    await client.post("/api/auth/signup", json=SIGNUP)
    client.cookies.clear()
    resp = await client.post("/api/auth/login", data={
        "username": "ALICE@example.com", "password": "Password123!"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.cookies


@pytest.mark.parametrize("creds", [
    {"username": "alice@example.com", "password": "wrong-password"},
    {"username": "nobody@example.com", "password": "Password123!"},
])
async def test_login_bad_credentials(client, creds):
    await client.post("/api/auth/signup", json=SIGNUP)
    resp = await client.post("/api/auth/login", data=creds)
    assert resp.status_code == 401


async def test_login_missing_fields(client):
    resp = await client.post("/api/auth/login", data={})
    assert resp.status_code == 422


# --- /me and token handling -----------------------------------------------

async def test_me_requires_auth(client):
    assert (await client.get("/api/auth/me")).status_code == 401


async def test_me_returns_current_user(make_user):
    c = await make_user("bob")
    resp = await c.get("/api/auth/me")
    assert resp.status_code == 200 and resp.json()["username"] == "bob"


def _token(sub="bob@example.com", key=None, alg="HS256", exp_delta=timedelta(hours=1), **extra):
    now = datetime.now(UTC)
    payload = {"sub": sub, "iat": now, "exp": now + exp_delta, **extra}
    return jwt.encode(payload, key or Token.secret_key, algorithm=alg)


@pytest.mark.parametrize("token", [
    "garbage",
    "a.b.c",
    "x",
    _token(key="wrong-key-wrong-key-wrong-key-wrong"),
    _token(exp_delta=timedelta(seconds=-10)),
    _token(sub="nobody@example.com"),
    jwt.encode({"sub": "bob@example.com"}, "x" * 32, algorithm="HS256"),
    jwt.encode({"sub": "bob@example.com", "exp": 9999999999}, None, algorithm="none"),
])
async def test_me_rejects_bad_tokens(make_user, client, token):
    await make_user("bob")
    resp = await client.get("/api/auth/me", headers={"Cookie": f"access_token={token}"})
    assert resp.status_code == 401


async def test_token_of_deleted_account_does_not_work_for_new_account_with_same_email(make_user, client):
    """JWTs are keyed on email and never revoked: deleting an account and
    re-registering the same email makes the old 30-day token valid again."""
    c = await make_user("bob")
    old_token = c.cookies.get("access_token")
    assert (await c.delete("/api/auth/me")).status_code == 200
    await make_user("bob")  # same email re-registered
    resp = await client.get("/api/auth/me", headers={"Cookie": f"access_token={old_token}"})
    assert resp.status_code == 401


async def test_logout_clears_cookie(make_user):
    c = await make_user()
    resp = await c.post("/api/auth/logout")
    assert resp.status_code == 200
    assert 'access_token=""' in resp.headers["set-cookie"] or "max-age=0" in resp.headers["set-cookie"].lower()


async def test_token_lifetime_is_reasonable():
    """30-day non-revocable tokens are long for a session cookie."""
    assert Token.access_token_expire_minutes <= 7 * 24 * 60


# --- RGPD deletion ----------------------------------------------------------

async def test_delete_account_removes_everything(make_user):
    a = await make_user("alice")
    b = await make_user("bob")
    await a.post("/api/friends/send_friend_request/bob")
    await b.post("/api/friends/accept_friend_request/alice")
    resp = await a.delete("/api/auth/me")
    assert resp.status_code == 200
    assert (await a.get("/api/auth/me")).status_code == 401
    assert (await b.get("/api/friends/friends_list")).json() == []
    async with db.async_session_factory() as s:
        assert await s.scalar(select(UserModel).where(UserModel.username == "alice")) is None


async def test_delete_account_requires_auth(client):
    assert (await client.delete("/api/auth/me")).status_code == 401


# --- 42 OAuth ---------------------------------------------------------------

class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text_data=None):
        self.status_code = status_code
        self._json = json_data
        self.text = text_data if text_data is not None else str(json_data)

    def json(self):
        if self._json is None:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._json


def fake_42_client(token_resp, me_resp=None, raise_on_post=None):
    class FakeClient:
        def __init__(self, *a, **kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **kw):
            if raise_on_post:
                raise raise_on_post
            return token_resp

        async def get(self, *a, **kw):
            return me_resp

    return FakeClient


ME_OK = {"email": "carol@student.42.fr", "login": "carol",
         "image": {"versions": {"medium": "https://cdn.intra.42.fr/users/x/medium_carol.jpg"}}}


async def _oauth_callback(client, monkeypatch, fake):
    monkeypatch.setattr(oauth_login, "AsyncClient", fake)
    start = await client.get("/api/auth/login_with_42")
    state = start.cookies.get("oauth_state")
    return await client.get(
        "/api/auth/login_with_42/callback", params={"code": "c", "state": state}
    )


async def test_oauth_start_redirects_with_state(client):
    resp = await client.get("/api/auth/login_with_42")
    assert resp.status_code == 307
    assert "state=" in resp.headers["location"]
    assert resp.cookies.get("oauth_state")


async def test_oauth_callback_requires_code_and_state(client):
    assert (await client.get("/api/auth/login_with_42/callback")).status_code == 400
    resp = await client.get("/api/auth/login_with_42/callback", params={"code": "x", "state": "y"})
    assert resp.status_code == 400


async def test_oauth_new_user(client, monkeypatch):
    fake = fake_42_client(FakeResponse(json_data={"access_token": "t"}), FakeResponse(json_data=ME_OK))
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 307
    assert resp.headers["location"].endswith("/profile")
    assert (await client.get("/api/auth/me")).json()["username"] == "carol"


async def test_oauth_returning_user(client, monkeypatch):
    fake = fake_42_client(FakeResponse(json_data={"access_token": "t"}), FakeResponse(json_data=ME_OK))
    await _oauth_callback(client, monkeypatch, fake)
    client.cookies.clear()
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 307


async def test_oauth_does_not_take_over_password_account(client, monkeypatch):
    await client.post("/api/auth/signup", json={**SIGNUP, "email": "carol@student.42.fr", "username": "carol"})
    client.cookies.clear()
    fake = fake_42_client(FakeResponse(json_data={"access_token": "t"}), FakeResponse(json_data=ME_OK))
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 403


async def test_oauth_legacy_user_with_null_email_verified_can_log_in(client, monkeypatch):
    """Users created by 42 OAuth before migration 5d803711036f have
    email_verified = NULL. They must still be able to log in with 42."""
    fake = fake_42_client(FakeResponse(json_data={"access_token": "t"}), FakeResponse(json_data=ME_OK))
    await _oauth_callback(client, monkeypatch, fake)
    async with db.async_session_factory() as s:
        await s.execute(update(UserModel).values(email_verified=None))
        await s.commit()
    client.cookies.clear()
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 307


@pytest.mark.parametrize("token_resp,me_resp", [
    (FakeResponse(status_code=500, text_data="boom"), None),
    (FakeResponse(json_data={}), None),
    (FakeResponse(json_data={"access_token": "t"}), FakeResponse(status_code=401, text_data="no")),
    (FakeResponse(json_data={"access_token": "t"}), FakeResponse(json_data={"login": "x"})),
])
async def test_oauth_upstream_errors_are_handled(client, monkeypatch, token_resp, me_resp):
    resp = await _oauth_callback(client, monkeypatch, fake_42_client(token_resp, me_resp))
    assert resp.status_code in (400, 502)


async def test_oauth_upstream_non_json_is_502(client, monkeypatch):
    fake = fake_42_client(FakeResponse(status_code=200, json_data=None, text_data="<html>"))
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 502


async def test_oauth_upstream_unreachable_is_502(client, monkeypatch):
    import httpx2
    fake = fake_42_client(None, raise_on_post=httpx2.ConnectError("down"))
    resp = await _oauth_callback(client, monkeypatch, fake)
    assert resp.status_code == 502


async def test_manually_set_valid_token_is_accepted(make_user, client):
    """Positive control for the cookie-injection tests above."""
    await make_user("bob")
    resp = await client.get("/api/auth/me", headers={"Cookie": f"access_token={_token()}"})
    assert resp.status_code == 200
