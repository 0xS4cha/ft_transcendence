from typing import Callable, Awaitable
import redis.exceptions as redis
from backend_app.core.dependencies import RedisDep
from pydantic import TypeAdapter

async def get_or_fetch[S](
    r: RedisDep,
    key: str,
    adapter: TypeAdapter[S],
    fetch_fn: Callable[[], Awaitable[S]],
    ttl: int = 900
) -> S:
    try:
        cached  = await r.get(key)
    except redis.RedisError:
        cached = None
    
    if cached is not None:
        return adapter.validate_json(cached)

    results = await fetch_fn();

    try:
        await r.set(key, adapter.dump_json(results), ex=ttl)
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