import asyncio

import pytest

from backend_app.core.websocket import wsConnectionManager

F = "/api/friends"


async def befriend(a, b, b_name, a_name):
    assert (await a.post(f"{F}/send_friend_request/{b_name}")).status_code == 201
    assert (await b.post(f"{F}/accept_friend_request/{a_name}")).status_code == 200


@pytest.mark.parametrize("method,path", [
    ("post", "/send_friend_request/x"),
    ("post", "/accept_friend_request/x"),
    ("delete", "/refuse_friend_request/x"),
    ("delete", "/remove_friend/x"),
    ("get", "/friend_requests_list"),
    ("get", "/friends_list"),
])
async def test_friends_endpoints_require_auth(client, method, path):
    resp = await getattr(client, method)(F + path)
    assert resp.status_code == 401


async def test_full_friendship_flow(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    assert (await a.post(f"{F}/send_friend_request/bob")).status_code == 201

    reqs = (await b.get(f"{F}/friend_requests_list")).json()
    assert [r["username"] for r in reqs] == ["alice"]
    assert (await a.get(f"{F}/friend_requests_list")).json() == []

    assert (await b.post(f"{F}/accept_friend_request/alice")).status_code == 200
    a_friends = (await a.get(f"{F}/friends_list")).json()
    b_friends = (await b.get(f"{F}/friends_list")).json()
    assert [f["username"] for f in a_friends] == ["bob"]
    assert [f["username"] for f in b_friends] == ["alice"]
    assert a_friends[0]["online"] is False

    assert (await a.delete(f"{F}/remove_friend/bob")).status_code == 200
    assert (await a.get(f"{F}/friends_list")).json() == []
    assert (await b.get(f"{F}/friends_list")).json() == []


async def test_send_request_to_self(make_user):
    a = await make_user("alice")
    assert (await a.post(f"{F}/send_friend_request/alice")).status_code == 400


async def test_send_request_to_unknown_user(make_user):
    a = await make_user("alice")
    assert (await a.post(f"{F}/send_friend_request/ghost")).status_code == 404


async def test_duplicate_requests(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    assert (await a.post(f"{F}/send_friend_request/bob")).status_code == 409
    assert (await b.post(f"{F}/send_friend_request/alice")).status_code == 409


async def test_request_to_existing_friend(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    await befriend(a, b, "bob", "alice")
    assert (await a.post(f"{F}/send_friend_request/bob")).status_code == 409


async def test_requester_cannot_accept_own_request(make_user):
    a, _b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    assert (await a.post(f"{F}/accept_friend_request/bob")).status_code == 404


async def test_third_party_cannot_accept(make_user):
    a, _b, c = await make_user("alice"), await make_user("bob"), await make_user("carol")
    await a.post(f"{F}/send_friend_request/bob")
    assert (await c.post(f"{F}/accept_friend_request/alice")).status_code == 404


async def test_refuse_request(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    assert (await b.delete(f"{F}/refuse_friend_request/alice")).status_code == 200
    assert (await b.get(f"{F}/friend_requests_list")).json() == []
    # can ask again after refusal
    assert (await a.post(f"{F}/send_friend_request/bob")).status_code == 201


@pytest.mark.parametrize("path", [
    "/accept_friend_request/alice", "/refuse_friend_request/alice", "/remove_friend/alice",
])
async def test_self_operations_rejected(make_user, path):
    a = await make_user("alice")
    method = "post" if "accept" in path else "delete"
    assert (await getattr(a, method)(F + path)).status_code == 400


async def test_remove_non_friend(make_user):
    a, _b = await make_user("alice"), await make_user("bob")
    assert (await a.delete(f"{F}/remove_friend/bob")).status_code == 404
    assert (await a.delete(f"{F}/remove_friend/ghost")).status_code == 404


async def test_pending_request_cannot_be_removed_as_friend(make_user):
    a, _b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    assert (await a.delete(f"{F}/remove_friend/bob")).status_code == 404


async def test_requester_can_cancel_pending_request(make_user):
    """There is no way for the sender to withdraw a pending request."""
    a, b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    statuses = [
        (await a.delete(f"{F}/remove_friend/bob")).status_code,
        (await a.delete(f"{F}/refuse_friend_request/bob")).status_code,
    ]
    assert 200 in statuses
    assert (await b.get(f"{F}/friend_requests_list")).json() == []


async def test_friends_list_does_not_leak_email(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    await befriend(a, b, "bob", "alice")
    friend = (await a.get(f"{F}/friends_list")).json()[0]
    assert "email" not in friend


async def test_friend_requests_list_does_not_leak_email(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    await a.post(f"{F}/send_friend_request/bob")
    req = (await b.get(f"{F}/friend_requests_list")).json()[0]
    assert "email" not in req


async def test_online_flag(make_user, app_state):
    a, b = await make_user("alice"), await make_user("bob")
    await befriend(a, b, "bob", "alice")
    await wsConnectionManager.redis.sadd(
        wsConnectionManager.ACTIVE_USERS_KEY, str(b.user["id"])
    )
    assert (await a.get(f"{F}/friends_list")).json()[0]["online"] is True


async def test_concurrent_mutual_requests_do_not_500(make_user):
    a, b = await make_user("alice"), await make_user("bob")
    r1, r2 = await asyncio.gather(
        a.post(f"{F}/send_friend_request/bob"),
        b.post(f"{F}/send_friend_request/alice"),
    )
    assert sorted([r1.status_code, r2.status_code]) == [201, 409]


async def test_send_request_db_error_does_not_leak_sql(make_user, monkeypatch):
    """IntegrityError text (SQL + constraint names) is echoed to the client."""
    from backend_app.api.endpoints.friends import send_friend_request as mod
    a, _b = await make_user("alice"), await make_user("bob")
    from sqlalchemy.exc import IntegrityError

    async def boom(*_a, **_kw):
        raise IntegrityError("INSERT INTO friends ...", {}, Exception("secret detail"))

    monkeypatch.setattr("sqlalchemy.ext.asyncio.AsyncSession.execute", boom)
    resp = await a.post(f"{F}/send_friend_request/bob")
    assert resp.status_code in (400, 409)
    assert "INSERT" not in resp.text and "secret" not in resp.text
    del mod
