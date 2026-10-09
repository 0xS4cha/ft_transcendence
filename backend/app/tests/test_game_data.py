"""Game data endpoints, with upstream (metatft / communitydragon / riot) faked
at the httpx2 transport level so the real parsing code runs."""

import copy

import httpx2
import pytest

from backend_app.api.endpoints.game_data import leaderboard as leaderboard_module
from backend_app.core.riot_api import riot_api

FILTER = {"queue": "1100", "rank": "GOLD,DIAMOND", "server": "EUW1"}

SET_DATA = {"setData": [{
    "mutator": "TFTSet18",
    "traits": [{"apiName": "TFT18_Bruiser", "name": "Bruiser",
                "effects": [{"minUnits": 2}, {"minUnits": 4}]}],
    "champions": [{"apiName": "Set18_Ahri", "name": "Ahri", "cost": 3, "traits": ["Bruiser"]}],
}]}
LOOKUP = {
    "items": [{"apiName": "TFT_Item_Rageblade", "name": "Rageblade", "composition": ["Bow", "Rod"]}],
    "augments": [{"apiName": "TFT_Aug_1", "name": "Golden Ticket", "rarity": "gold",
                  "rounds": ["2-1"], "icon": "GoldenTicket"}],
}
PLACES = [5, 4, 3, 3, 2, 2, 1, 1]
RESULTS = {
    "traits": {"results": [{"trait": "TFT18_Bruiser_1", "places": PLACES}]},
    "units": {"results": [{"unit": "Set18_Ahri", "places": PLACES}]},
    "items_matches": {"results": [{"itemName": "TFT_Item_Rageblade", "places": PLACES}]},
}


def upstream(monkeypatch, overrides=None):
    """Route httpx2 requests by URL fragment. overrides: {fragment: (status, json|bytes)}"""
    routes = dict(overrides or {})
    routes |= {k: v for k, v in {
        "communitydragon": (200, SET_DATA),
        "lookups/": (200, LOOKUP),
        "tft-stat-api/traits": (200, RESULTS["traits"]),
        "tft-stat-api/units": (200, RESULTS["units"]),
        "tft-stat-api/items_matches": (200, RESULTS["items_matches"]),
    }.items() if k not in routes}
    calls = []

    async def send(self, request, **_kw):
        url = str(request.url)
        calls.append(url)
        for frag, (status, body) in routes.items():
            if frag in url:
                if isinstance(body, Exception):
                    raise body
                if isinstance(body, bytes):
                    return httpx2.Response(status, content=body, request=request)
                return httpx2.Response(status, json=body, request=request)
        raise AssertionError(f"unexpected upstream call {url}")

    monkeypatch.setattr(httpx2.AsyncClient, "send", send)
    return calls


# --- happy paths ------------------------------------------------------------

async def test_items(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/game_data/items_data", params=FILTER)
    assert resp.status_code == 200
    item = resp.json()[0]
    assert item["name"] == "Rageblade" and item["frequency"] == 100
    assert 0 < item["winrate"] < 100 and 1 <= item["avg_place"] <= 8


async def test_traits(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/game_data/traits_data", params=FILTER)
    assert resp.status_code == 200
    assert resp.json()[0]["breakpoint"] == "2"


async def test_units(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/game_data/units_data", params=FILTER)
    assert resp.status_code == 200
    unit = resp.json()[0]
    assert unit["name"] == "Ahri" and unit["traits"][0]["name"] == "Bruiser"


async def test_augments(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/game_data/augments_data")
    assert resp.status_code == 200 and resp.json()[0]["name"] == "Golden Ticket"


async def test_results_are_cached_in_redis(client, monkeypatch):
    calls = upstream(monkeypatch)
    await client.get("/api/game_data/items_data", params=FILTER)
    n = len(calls)
    await client.get("/api/game_data/items_data", params=FILTER)
    assert len(calls) == n


async def test_filter_order_shares_cache(client, monkeypatch):
    calls = upstream(monkeypatch)
    await client.get("/api/game_data/items_data", params=FILTER)
    n = len(calls)
    await client.get("/api/game_data/items_data", params={**FILTER, "rank": "DIAMOND,GOLD"})
    assert len(calls) == n


# --- validation -------------------------------------------------------------

@pytest.mark.parametrize("endpoint", ["items_data", "traits_data", "units_data"])
@pytest.mark.parametrize("params", [
    {"queue": "9999", "rank": "GOLD", "server": "EUW1"},
    {"queue": "1100", "rank": "WOOD", "server": "EUW1"},
    {"queue": "1100", "rank": "GOLD", "server": "MARS"},
    {"queue": "1100", "rank": "", "server": "EUW1"},
    {"queue": "1100", "rank": "GOLD,", "server": "EUW1"},
], ids=["queue", "rank", "server", "empty-rank", "trailing-comma"])
async def test_invalid_filters(client, endpoint, params):
    resp = await client.get(f"/api/game_data/{endpoint}", params=params)
    assert resp.status_code == 400


@pytest.mark.parametrize("endpoint", ["items_data", "traits_data", "units_data"])
async def test_missing_filters(client, endpoint):
    assert (await client.get(f"/api/game_data/{endpoint}")).status_code == 422


# --- upstream failures must be 502, never 500 --------------------------------

ENDPOINTS = ["items_data", "traits_data", "units_data", "augments_data"]


@pytest.mark.parametrize("endpoint", ENDPOINTS)
async def test_upstream_http_error(client, monkeypatch, endpoint):
    upstream(monkeypatch, {"metatft": (503, {"x": 1}), "communitydragon": (503, {"x": 1})})
    resp = await client.get(f"/api/game_data/{endpoint}", params=FILTER)
    assert resp.status_code == 502


@pytest.mark.parametrize("endpoint", ENDPOINTS)
async def test_upstream_unreachable(client, monkeypatch, endpoint):
    err = httpx2.ConnectError("down")
    upstream(monkeypatch, {"metatft": (0, err), "communitydragon": (0, err)})
    resp = await client.get(f"/api/game_data/{endpoint}", params=FILTER)
    assert resp.status_code == 502


@pytest.mark.parametrize("endpoint", ENDPOINTS)
async def test_upstream_returns_html(client, monkeypatch, endpoint):
    """e.g. a Cloudflare challenge page with status 200."""
    html = b"<html>Just a moment...</html>"
    upstream(monkeypatch, {"metatft": (200, html), "communitydragon": (200, html)})
    resp = await client.get(f"/api/game_data/{endpoint}", params=FILTER)
    assert resp.status_code == 502


@pytest.mark.parametrize("endpoint", ["items_data", "traits_data", "units_data"])
async def test_upstream_returns_json_list_instead_of_object(client, monkeypatch, endpoint):
    upstream(monkeypatch, {"tft-stat-api": (200, [])})
    resp = await client.get(f"/api/game_data/{endpoint}", params=FILTER)
    assert resp.status_code == 502


async def test_unit_with_zero_games_is_skipped(client, monkeypatch):
    results = {"results": [
        {"unit": "Set18_Ahri", "places": PLACES},
        {"unit": "Set18_Ahri", "places": [0] * 8},
    ]}
    upstream(monkeypatch, {"tft-stat-api/units": (200, results)})
    resp = await client.get("/api/game_data/units_data", params=FILTER)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_unit_missing_cost_is_skipped(client, monkeypatch):
    data = copy.deepcopy(SET_DATA)
    data["setData"][0]["champions"].append({"apiName": "Set18_Zed", "name": "Zed"})
    results = {"results": [{"unit": "Set18_Ahri", "places": PLACES},
                           {"unit": "Set18_Zed", "places": PLACES}]}
    upstream(monkeypatch, {"communitydragon": (200, data), "tft-stat-api/units": (200, results)})
    resp = await client.get("/api/game_data/units_data", params=FILTER)
    assert resp.status_code == 200
    assert [u["name"] for u in resp.json()] == ["Ahri"]


async def test_trait_with_non_numeric_suffix(client, monkeypatch):
    results = {"results": [{"trait": "TFT18_Bruiser_1", "places": PLACES},
                           {"trait": "TFT18_Bruiser_x", "places": PLACES}]}
    upstream(monkeypatch, {"tft-stat-api/traits": (200, results)})
    resp = await client.get("/api/game_data/traits_data", params=FILTER)
    assert resp.status_code == 200


async def test_places_with_null_values(client, monkeypatch):
    results = {"results": [{"itemName": "TFT_Item_Rageblade", "places": [1, None, 2, 0, 0, 0, 0, 0]}]}
    upstream(monkeypatch, {"tft-stat-api/items_matches": (200, results)})
    resp = await client.get("/api/game_data/items_data", params=FILTER)
    assert resp.status_code in (200, 502)


async def test_missing_3d_model_is_null_not_string_none(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/game_data/units_data", params=FILTER)
    assert resp.json()[0]["model"] != "models_3d/None"


# --- leaderboard ------------------------------------------------------------

class FakeAiohttpResp:
    status = 200

    def __init__(self, data=None, exc=None):
        self.data, self.exc = data, exc

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def json(self):
        if self.exc:
            raise self.exc
        return self.data


def fake_aiohttp(monkeypatch, data=None, exc=None, calls=None):
    class Session:
        def __init__(self, *_a, **_kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        def get(self, url, **_kw):
            if calls is not None:
                calls.append(url)
            return FakeAiohttpResp(data, exc)

    monkeypatch.setattr(leaderboard_module.aiohttp, "ClientSession", Session)


async def test_leaderboard(client, monkeypatch):
    fake_aiohttp(monkeypatch, data={"players": [1, 2]})
    resp = await client.get("/api/leaderboard/", params={"server": "euw1"})
    assert resp.status_code == 200 and resp.json() == {"players": [1, 2]}


async def test_leaderboard_invalid_server(client):
    assert (await client.get("/api/leaderboard/", params={"server": "mars"})).status_code == 400


async def test_leaderboard_refreshes_after_20_seconds(client, monkeypatch):
    """REFRESH_INTERVAL_MS (20000) is compared with time.time() in seconds,
    so the cache actually lives 20000 s (5.5 h)."""
    calls = []
    fake_aiohttp(monkeypatch, data={"players": []}, calls=calls)
    now = [1_000_000.0]
    monkeypatch.setattr(leaderboard_module.time, "time", lambda: now[0])
    await client.get("/api/leaderboard/")
    now[0] += 60
    await client.get("/api/leaderboard/")
    assert len(calls) == 2


async def test_leaderboard_upstream_error_is_502(client, monkeypatch):
    import aiohttp
    fake_aiohttp(monkeypatch, exc=aiohttp.ContentTypeError(None, ()))
    resp = await client.get("/api/leaderboard/")
    assert resp.status_code == 502


async def test_leaderboard_error_body_not_cached(client, monkeypatch):
    calls = []
    fake_aiohttp(monkeypatch, data={"error": "rate limited"}, calls=calls)
    await client.get("/api/leaderboard/")
    fake_aiohttp(monkeypatch, data={"players": [1]}, calls=calls)
    resp = await client.get("/api/leaderboard/")
    assert resp.json() == {"players": [1]}


# --- patchnote --------------------------------------------------------------

@pytest.mark.parametrize("lang", ["EN", "fr", " es "])
async def test_patchnote(client, lang):
    resp = await client.get("/api/patchnote/latest", params={"lang": lang})
    assert resp.status_code == 200 and "<" in resp.text


async def test_patchnote_invalid_lang(client):
    assert (await client.get("/api/patchnote/latest", params={"lang": "../../etc/passwd"})).status_code == 400


# --- search -----------------------------------------------------------------

async def test_search_game_data(client, monkeypatch):
    upstream(monkeypatch)
    resp = await client.get("/api/search/ahr")
    assert resp.status_code == 200
    body = resp.json()
    assert [u["name"] for u in body["unit"]] == ["Ahri"]
    assert body["user"] == []


async def test_search_user_not_found_returns_empty_list(client, monkeypatch):
    upstream(monkeypatch)

    async def none(*_a, **_kw):
        return None
    monkeypatch.setattr(riot_api, "riot_get", none)
    body = (await client.get("/api/search/Someone%23EUW")).json()
    assert body["user"] == []


async def test_search_user_found(client, monkeypatch):
    upstream(monkeypatch)

    async def riot_get(url, server, params=None):
        if "by-riot-id" in url:
            return {"puuid": "p", "gameName": "Foo", "tagLine": "EUW"}
        if "region" in url:
            return {"region": "euw1"}
        if "summoners" in url:
            return {"puuid": "p", "profileIconId": 1, "summonerLevel": 100}
        return [{"tier": "GOLD", "rank": "II", "leaguePoints": 10, "wins": 5, "losses": 5}]
    monkeypatch.setattr(riot_api, "riot_get", riot_get)
    body = (await client.get("/api/search/Foo%23EUW")).json()
    assert body["user"][0]["tier"] == "GOLD"


async def test_search_uses_correct_riot_routing(monkeypatch):
    from backend_app.api.endpoints.game_data.search import Platform
    assert Platform.NA1.get_continent() == "americas"
    assert Platform.KR.get_continent() == "asia"


async def test_search_upstream_down_still_200(client):
    resp = await client.get("/api/search/anything")
    assert resp.status_code == 200
