from httpx2 import AsyncClient
from typing import Any, Callable, Awaitable
import redis.asyncio as redis
from pydantic import TypeAdapter, ValidationError
from backend_app.core.dependencies import RedisDep

async def get_game_data(
    r: redis.Redis,
    key: str,
    fetch_fn: Callable[[], Awaitable[dict[str, Any]]],
    ttl: int = 3600
) -> dict[str, Any] | None:
    key = "metatft:" + key
    adapter = TypeAdapter(dict[str, Any])
    
    return await get_or_fetch(r, key, adapter, fetch_fn, ttl)


async def fetch_lookup(
    client: AsyncClient
) -> dict[str, Any]:
    resp = await client.get("https://data.metatft.com/lookups/TFTSet18_latest_en_us.json")
    resp.raise_for_status()

    return resp.json()

async def fetch_set_data(
    client: AsyncClient
) -> dict[str, Any] | None:
    resp = await client.get("https://raw.communitydragon.org/latest/cdragon/tft/en_us.json")
    resp.raise_for_status()
    
    return next((entry for entry in resp.json().get("setData", []) if entry.get("mutator", "") == "TFTSet18"), None)

async def get_or_fetch[T](
    r: RedisDep,
    key: str,
    adapter: TypeAdapter[T],
    fetch_fn: Callable[[], Awaitable[T]],
    ttl: int = 900
) -> T:
    try:
        cached  = await r.get(key)
    except redis.RedisError:
        cached = None
    
    if cached is not None:
        try:
            return adapter.validate_json(cached)
        except ValidationError:
            pass


    results = await fetch_fn();

    try:
        adapted = adapter.dump_json(results)
    except (TypeError, ValidationError):
        return results

    try:
        await r.set(key, adapted, ex=ttl)
    except redis.RedisError :
        pass

    return results

def build_cache_key(
    id: str,
    queue: str,
    ranks: str,
    servers: str,
) -> str:
    return f"metatft:{id}:{queue}:{ranks}:{servers}"