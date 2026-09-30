from typing import Callable, Awaitable
import redis.exceptions as redis
from backend_app.core.dependencies import RedisDep
from pydantic import TypeAdapter, ValidationError

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