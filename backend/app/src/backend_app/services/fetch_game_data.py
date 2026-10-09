import logging
from collections.abc import Awaitable, Callable
from typing import Any

import redis.asyncio as redis
from httpx2 import AsyncClient, HTTPError, Response
from pydantic import TypeAdapter, ValidationError

from backend_app.core.dependencies import RedisDep

logger = logging.getLogger(__name__)


async def get_game_data(
    r: redis.Redis,
    key: str,
    fetch_fn: Callable[[], Awaitable[dict[str, Any]]],
    ttl: int = 3600
) -> dict[str, Any] | None:
    key = "metatft:" + key
    adapter = TypeAdapter(dict[str, Any])
    
    return await get_or_fetch(r, key, adapter, fetch_fn, ttl)


class UpstreamDataError(HTTPError):
    pass


def json_object(resp: Response) -> dict[str, Any]:
    try:
        data = resp.json()
    except ValueError as e:
        raise UpstreamDataError(f"Invalid JSON from {resp.request.url}") from e
    if not isinstance(data, dict):
        raise UpstreamDataError(f"Unexpected JSON shape from {resp.request.url}")
    return data


def dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, dict)]


async def fetch_lookup(
    client: AsyncClient
) -> dict[str, Any]:
    resp = await client.get("https://data.metatft.com/lookups/TFTSet18_latest_en_us.json")
    resp.raise_for_status()

    return json_object(resp)

async def fetch_set_data(
    client: AsyncClient
) -> dict[str, Any] | None:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()

    set_data = dict_list(json_object(resp).get("setData"))
    return next((entry for entry in set_data if entry.get("mutator") == "TFTSet18"), None)

async def fetch_results(
    client: AsyncClient,
    key: str,
    queue: str,
    ranks: str,
    servers: str,
) -> list[dict[str, Any]] | None:
    resp = await client.get(f"https://api-hc.metatft.com/tft-stat-api/{key}?queue={queue}&rank={ranks}&server={servers}")
    resp.raise_for_status()

    results = json_object(resp).get("results")
    if results is None:
        return None
    return dict_list(results)

async def get_or_fetch[T](
    r: RedisDep,
    key: str,
    adapter: TypeAdapter[T],
    fetch_fn: Callable[[], Awaitable[T]],
    ttl: int = 900
) -> T:
    try:
        cached  = await r.get(key)
    except redis.RedisError as e:
        logger.warning(f"[get_or_fetch] Redis GET failed for {key}: {e}")
        cached = None
    
    if cached is not None:
        try:
            return adapter.validate_json(cached)
        except ValidationError as e:
            logger.warning(f"[get_or_fetch] cache validation failed for {key}, refetching: {e}")


    results = await fetch_fn()

    try:
        adapted = adapter.dump_json(results)
    except (TypeError, ValidationError) as e:
        logger.warning(f"[get_or_fetch] serialize failed for {key}, not caching: {e}")
        return results

    try:
        await r.set(key, adapted, ex=ttl)
    except redis.RedisError as e:
        logger.warning(f"[get_or_fetch] Redis SET failed for {key}: {e}")

    return results

def build_cache_key(
    id: str,
    queue: str,
    ranks: str,
    servers: str,
) -> str:
    return f"metatft:{id}:{queue}:{ranks}:{servers}"