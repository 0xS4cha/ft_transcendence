import os

import pytest
from conftest import image_bytes

U = "/api/user"
PICTURES = "/app/src/shared/profile_pictures"


# --- change_username --------------------------------------------------------

async def test_change_username(make_user):
    a = await make_user("alice")
    resp = await a.post(f"{U}/change_username", params={"new_username": "alicia"})
    assert resp.status_code == 200 and resp.json()["username"] == "alicia"


async def test_change_username_same(make_user):
    a = await make_user("alice")
    resp = await a.post(f"{U}/change_username", params={"new_username": "alice"})
    assert resp.status_code == 409


async def test_change_username_taken(make_user):
    a, _b = await make_user("alice"), await make_user("bob")
    resp = await a.post(f"{U}/change_username", params={"new_username": "bob"})
    assert resp.status_code == 409


async def test_change_username_requires_auth(client):
    resp = await client.post(f"{U}/change_username", params={"new_username": "x"})
    assert resp.status_code == 401


@pytest.mark.parametrize("name", ["", "ab", "a" * 33, "a" * 5000, "a/b", "../x", "   ", "<img src=x>"], ids=["empty", "2chars", "33chars", "5000chars", "slash", "dotdot", "spaces", "html"])
async def test_change_username_validates_like_signup(make_user, name):
    """Signup enforces 3..32 chars; change_username accepts anything."""
    a = await make_user("alice")
    resp = await a.post(f"{U}/change_username", params={"new_username": name})
    assert resp.status_code == 422


# --- change_picture ---------------------------------------------------------

async def upload(c, data, filename="p.png", ctype="image/png"):
    return await c.post(f"{U}/change_picture", files={"file": (filename, data, ctype)})


@pytest.mark.parametrize("fmt", ["PNG", "JPEG"])
async def test_change_picture_valid(make_user, fmt):
    a = await make_user()
    resp = await upload(a, image_bytes(fmt))
    assert resp.status_code == 200
    pic = resp.json()["picture"]
    assert pic.startswith("profile_pictures/") and pic.endswith(".webp")
    assert os.path.exists(os.path.join("/app/src/shared", pic))


async def test_change_picture_rgba_png(make_user):
    a = await make_user()
    assert (await upload(a, image_bytes("PNG", mode="RGBA"))).status_code == 200


async def test_change_picture_replaces_old_file(make_user):
    a = await make_user()
    first = (await upload(a, image_bytes())).json()["picture"]
    second = (await upload(a, image_bytes())).json()["picture"]
    assert first != second
    assert not os.path.exists(os.path.join("/app/src/shared", first))


async def test_change_picture_gif_rejected(make_user):
    a = await make_user()
    assert (await upload(a, image_bytes("GIF"), "x.gif", "image/gif")).status_code == 415


@pytest.mark.parametrize("data", [b"", b"not an image", b"\x89PNG\r\n\x1a\n" + b"\x00" * 100])
async def test_change_picture_garbage(make_user, data):
    a = await make_user()
    assert (await upload(a, data)).status_code == 400


async def test_change_picture_svg_with_script_rejected(make_user):
    a = await make_user()
    svg = b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>'
    assert (await upload(a, svg, "x.svg", "image/svg+xml")).status_code == 400


async def test_change_picture_too_large(make_user):
    a = await make_user()
    data = image_bytes() + b"\x00" * (5 * 1024 * 1024)
    assert (await upload(a, data)).status_code == 413


async def test_change_picture_decompression_bomb(make_user):
    a = await make_user()
    bomb = image_bytes("PNG", size=(6000, 6000), mode="1")
    assert len(bomb) < 5 * 1024 * 1024
    resp = await upload(a, bomb)
    assert resp.status_code in (400, 413)


async def test_change_picture_missing_file(make_user):
    a = await make_user()
    assert (await a.post(f"{U}/change_picture")).status_code == 422


async def test_change_picture_requires_auth(client):
    assert (await upload(client, image_bytes())).status_code == 401


# --- remove_picture ---------------------------------------------------------

async def test_remove_picture(make_user):
    a = await make_user()
    pic = (await upload(a, image_bytes())).json()["picture"]
    resp = await a.delete(f"{U}/remove_picture")
    assert resp.status_code == 200 and resp.json()["picture"] is None
    assert not os.path.exists(os.path.join("/app/src/shared", pic))
    assert (await a.delete(f"{U}/remove_picture")).status_code == 409


async def test_remove_picture_without_one(make_user):
    a = await make_user()
    assert (await a.delete(f"{U}/remove_picture")).status_code == 409


async def test_delete_account_removes_picture_file(make_user):
    """RGPD: the uploaded picture should be erased with the account."""
    a = await make_user()
    pic = (await upload(a, image_bytes())).json()["picture"]
    await a.delete("/api/auth/me")
    assert not os.path.exists(os.path.join("/app/src/shared", pic))


async def test_uploaded_picture_is_served(make_user):
    a = await make_user()
    pic = (await upload(a, image_bytes())).json()["picture"]
    resp = await a.get(f"/api/public/{pic}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/webp"


async def test_static_files_no_path_traversal(client):
    for path in ["/api/public/profile_pictures/../database.py",
                 "/api/public/profile_pictures/%2e%2e/database.py",
                 "/api/public/models_3d/..%2f..%2fdatabase.py"]:
        resp = await client.get(path)
        assert resp.status_code == 404, path
