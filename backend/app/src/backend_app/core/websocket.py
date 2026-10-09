import asyncio
import contextlib
import datetime
import json
import logging

import redis.asyncio as redis
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebsocketConnectionManager:
    REDIS_CHANNEL = "websocket:broadcast"
    ACTIVE_USERS_KEY = "websocket:active_users"

    def __init__(self, redis_url: str):
        self.connections: set[tuple[int, WebSocket]] = set()
        self.lock = asyncio.Lock()
        self.redis = redis.from_url(
            redis_url,
            decode_responses=True,
        )
        self._listener_task: asyncio.Task | None = None

    @staticmethod
    def _json_default(obj: object):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        try:
            return str(obj)
        except Exception as e:
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable") from e

    async def start(self):
        self._listener_task = asyncio.create_task(self._redis_listener())

    async def stop(self):
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        await self.redis.aclose()

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        async with self.lock:
            self.connections.add((client_id, websocket))

        user_connections_key = f"websocket:users:{client_id}"
        websocket_key = str(id(websocket))
        await self.redis.sadd(user_connections_key, websocket_key)

        if await self.redis.scard(user_connections_key) == 1:
            await self.redis.sadd(self.ACTIVE_USERS_KEY, str(client_id))

    async def disconnect(self, websocket: WebSocket, client_id: int):
        async with self.lock:
            self.connections.discard((client_id, websocket))

        user_connections_key = f"websocket:users:{client_id}"
        websocket_key = str(id(websocket))
        await self.redis.srem(user_connections_key, websocket_key)

        if await self.redis.scard(user_connections_key) == 0:
            await self.redis.srem(self.ACTIVE_USERS_KEY, str(client_id))

    async def broadcast(self, message: dict, user_ids: list[int] | None = None):
        payload = {
            "message": message,
            "user_ids": user_ids,
        }

        await self.redis.publish(
            self.REDIS_CHANNEL,
            json.dumps(payload, default=self._json_default),
        )

    async def _redis_listener(self):
        backoff = 1
        while True:
            pubsub = self.redis.pubsub()
            try:
                await pubsub.subscribe(self.REDIS_CHANNEL)
                backoff = 1
                async for item in pubsub.listen():
                    if item["type"] != "message":
                        continue
                    await self._handle_pubsub_message(item["data"])
            except asyncio.CancelledError:
                raise
            except (redis.RedisError, OSError) as e:
                logger.warning(f"[websocket] pub/sub listener error, reconnecting in {backoff}s: {e!r}")
            finally:
                with contextlib.suppress(Exception):
                    await pubsub.aclose()
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)

    async def _handle_pubsub_message(self, data: str):
        try:
            payload = json.loads(data)
            message = payload["message"]
            user_ids = payload["user_ids"]
        except (ValueError, TypeError, KeyError) as e:
            logger.warning(f"[websocket] ignoring malformed broadcast: {e!r}")
            return
        await self._broadcast_local(message=message, user_ids=user_ids)

    async def _broadcast_local(self, message: dict, user_ids: list[int] | None = None,):
        async with self.lock:
            connections = list(self.connections)

        if user_ids is not None:
            user_ids_set = set(user_ids)

            connections = [
                (user_id, websocket)
                for user_id, websocket in connections
                if user_id in user_ids_set
            ]

        async def send(user_id: int, websocket: WebSocket):
            try:
                await websocket.send_json(message)
            except Exception:  # noqa: BLE001
                await self.disconnect(websocket, user_id)
        await asyncio.gather(*(send(user_id, websocket) for user_id, websocket in connections))

    async def local_connection_count(self) -> int:
        async with self.lock:
            return len(self.connections)


wsConnectionManager = WebsocketConnectionManager("redis://redis:6379")
async def WSbroadcast(type: str, data: dict, user_ids: list[int] | None = None) -> int:
    await wsConnectionManager.broadcast(
        {
            "type": type,
            "data": data,
        },
        user_ids,
    )
    if user_ids is not None:
        return len(user_ids)
    return await wsConnectionManager.local_connection_count()
