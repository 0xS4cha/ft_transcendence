import pytest

from backend_app.api.endpoints.chat import chatbot as chatbot_module
from conftest import image_bytes

C = "/api/chat"


async def test_chat_requires_auth(client):
    assert (await client.get(f"{C}/messages")).status_code == 401
    assert (await client.post(f"{C}/send", json={"content": "hi"})).status_code == 401


async def test_send_message_user_with_uploaded_picture(make_user):
    a = await make_user()
    await a.post("/api/user/change_picture", files={"file": ("p.png", image_bytes(), "image/png")})
    resp = await a.post(f"{C}/send", json={"content": "hello"})
    assert resp.status_code == 200
    assert resp.json()["picture"].startswith("/api/public/profile_pictures/")


async def test_send_message_user_without_picture(make_user):
    """Every password-signup user has picture=None."""
    a = await make_user()
    resp = await a.post(f"{C}/send", json={"content": "hello"})
    assert resp.status_code == 200


async def test_messages_survive_a_user_without_picture(make_user):
    """If one message author has no picture, /messages must not break for everyone."""
    a, b = await make_user("alice"), await make_user("bob")
    try:
        await a.post(f"{C}/send", json={"content": "hello"})
    except TypeError:
        pass  # the send itself crashes after committing (see test above)
    resp = await b.get(f"{C}/messages")
    assert resp.status_code == 200
    assert [m["content"] for m in resp.json()] == ["hello"]


async def test_send_and_list_messages_order(make_user):
    a = await make_user()
    await a.post("/api/user/change_picture", files={"file": ("p.png", image_bytes(), "image/png")})
    for i in range(3):
        await a.post(f"{C}/send", json={"content": f"m{i}"})
    from backend_app.api.endpoints.chat import chat
    chat.last_refresh_timestamp = 0
    msgs = (await a.get(f"{C}/messages")).json()
    assert [m["content"] for m in msgs] == ["m0", "m1", "m2"]


async def test_send_returns_message_id_not_user_id(make_user):
    a = await make_user()
    await a.post("/api/user/change_picture", files={"file": ("p.png", image_bytes(), "image/png")})
    first = (await a.post(f"{C}/send", json={"content": "1"})).json()
    second = (await a.post(f"{C}/send", json={"content": "2"})).json()
    assert first["id"] != second["id"]


@pytest.mark.parametrize("body", [{}, {"content": ""}, {"content": None}])
async def test_empty_message_is_400_not_401(make_user, body):
    """401 on an empty message can make the frontend think the session expired."""
    a = await make_user()
    resp = await a.post(f"{C}/send", json=body)
    assert resp.status_code in (400, 422)


async def test_message_length_is_limited(make_user):
    a = await make_user()
    await a.post("/api/user/change_picture", files={"file": ("p.png", image_bytes(), "image/png")})
    resp = await a.post(f"{C}/send", json={"content": "x" * 1_000_000})
    assert resp.status_code in (413, 422)


async def test_whitespace_only_message_rejected(make_user):
    a = await make_user()
    await a.post("/api/user/change_picture", files={"file": ("p.png", image_bytes(), "image/png")})
    resp = await a.post(f"{C}/send", json={"content": "   \n  "})
    assert resp.status_code in (400, 422)


async def test_send_malformed_json(make_user):
    a = await make_user()
    resp = await a.post(f"{C}/send", content=b"{not json", headers={"content-type": "application/json"})
    assert resp.status_code == 422


# --- chatbot ----------------------------------------------------------------

async def test_chatbot_requires_auth(client):
    assert (await client.get("/api/chatbot/ask", params={"message": "hi"})).status_code == 401


async def test_chatbot_answers(make_user, monkeypatch):
    async def fake_chat(**_kw):
        return {"message": {"content": "Use Rageblade."}}
    monkeypatch.setattr(chatbot_module.chatbot.client, "chat", fake_chat)
    a = await make_user()
    resp = await a.get("/api/chatbot/ask", params={"message": "best item for carry?"})
    assert resp.status_code == 200 and resp.json() == "Use Rageblade."


async def test_chatbot_ollama_down_returns_message(make_user, monkeypatch):
    async def down(**_kw):
        raise ConnectionError("ollama down")
    monkeypatch.setattr(chatbot_module.chatbot.client, "chat", down)
    a = await make_user()
    resp = await a.get("/api/chatbot/ask", params={"message": "hi"})
    assert resp.status_code == 200


@pytest.mark.parametrize("message", ["", " ", "???", "a" * 6000, "\x00"], ids=["empty", "space", "punct", "long", "nul"])
async def test_chatbot_odd_input_no_500(make_user, monkeypatch, message):
    async def fake_chat(**_kw):
        return {"message": {"content": "ok"}}
    monkeypatch.setattr(chatbot_module.chatbot.client, "chat", fake_chat)
    a = await make_user()
    resp = await a.get("/api/chatbot/ask", params={"message": message})
    assert resp.status_code < 500


async def test_chatbot_message_length_limited(make_user, monkeypatch):
    async def fake_chat(**_kw):
        return {"message": {"content": "ok"}}
    monkeypatch.setattr(chatbot_module.chatbot.client, "chat", fake_chat)
    a = await make_user()
    resp = await a.get("/api/chatbot/ask", params={"message": "a" * 20_000})
    assert resp.status_code in (413, 422)
