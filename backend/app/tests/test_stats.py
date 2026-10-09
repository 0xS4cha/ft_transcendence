import asyncio
import time

import pytest
import requests

from backend_app.api.endpoints.stats import stats as stats_module


class FakeResp:
    def __init__(self, data, status=200):
        self.data, self.status_code = data, status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))

    def json(self):
        if isinstance(self.data, Exception):
            raise self.data
        return self.data


GRAPHQL_OK = {"data": {"getPlatformStats": {"totalMatches": 42, "milestones": {"goldWasted": 7}}}}


def fake_post(monkeypatch, result):
    def post(*_a, **_kw):
        if isinstance(result, Exception):
            raise result
        return result
    monkeypatch.setattr(stats_module.requests, "post", post)


async def test_home_stats(client, monkeypatch):
    fake_post(monkeypatch, FakeResp(GRAPHQL_OK))
    resp = await client.get("/api/stats/home")
    assert resp.status_code == 200
    body = resp.json()
    assert body["matchCount"] == 42 and body["goldCount"] == 7
    assert len(body["history"]) == 90


async def test_accounts_created(client, make_user, monkeypatch):
    fake_post(monkeypatch, FakeResp(GRAPHQL_OK))
    await make_user()
    await make_user()
    assert (await client.get("/api/stats/accounts_created")).json() == {"count": 2}


async def test_unknown_stat(client, monkeypatch):
    fake_post(monkeypatch, FakeResp(GRAPHQL_OK))
    assert (await client.get("/api/stats/nope")).status_code == 404


@pytest.mark.parametrize("failure", [
    requests.ConnectionError("down"),
    requests.Timeout("slow"),
    FakeResp(ValueError("not json")),
    FakeResp({"data": None}),
    FakeResp({"errors": ["x"]}),
    FakeResp({"data": {"getPlatformStats": None}}),
], ids=["conn", "timeout", "html", "data-null", "no-data", "stats-null"])
async def test_upstream_stats_failure_does_not_500(client, monkeypatch, failure):
    fake_post(monkeypatch, failure)
    resp = await client.get("/api/stats/home")
    assert resp.status_code == 200


async def test_upstream_stats_call_has_timeout(client, monkeypatch):
    seen = {}

    def post(*_a, **kw):
        seen.update(kw)
        return FakeResp(GRAPHQL_OK)
    monkeypatch.setattr(stats_module.requests, "post", post)
    await client.get("/api/stats/home")
    assert "timeout" in seen


async def test_slow_upstream_does_not_block_event_loop(client, monkeypatch):
    """requests.post is synchronous: while it waits, no other request is served."""
    def slow_post(*_a, **_kw):
        time.sleep(1.0)
        raise requests.Timeout()
    monkeypatch.setattr(stats_module.requests, "post", slow_post)

    async def health_latency():
        await asyncio.sleep(0.1)
        t = time.perf_counter()
        await client.get("/health")
        return time.perf_counter() - t

    _, latency = await asyncio.gather(client.get("/api/stats/home"), health_latency())
    assert latency < 0.5


async def test_failed_upstream_is_not_retried_on_every_request(client, monkeypatch):
    calls = []

    def post(*_a, **_kw):
        calls.append(1)
        raise requests.HTTPError()
    monkeypatch.setattr(stats_module.requests, "post", post)
    for _ in range(5):
        await client.get("/api/stats/accounts_created")
    assert len(calls) <= 1


async def test_get_does_not_inflate_visit_counter(client, monkeypatch):
    """Every GET /stats/visits or /stats/home adds a visit; a script can inflate it."""
    fake_post(monkeypatch, FakeResp(GRAPHQL_OK))
    for _ in range(10):
        await client.get("/api/stats/visits")
    count = (await client.get("/api/stats/visits")).json()["count"]
    assert count <= 2
