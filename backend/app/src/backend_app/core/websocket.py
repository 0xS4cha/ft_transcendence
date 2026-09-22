import asyncio
import json

import redis.asyncio as redis
from fastapi import WebSocket


class WebsocketConnectionManager:
    REDIS_CHANNEL = "websocket:broadcast"

    def __init__(self, redis_url: str):
        self.connections: set[tuple[int, WebSocket]] = set()
        self.lock = asyncio.Lock()
        self.redis = redis.from_url(
            redis_url,
            decode_responses=True,
        )
        self._listener_task: asyncio.Task | None = None

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

    async def disconnect(self, websocket: WebSocket, client_id: int):
        async with self.lock:
            self.connections.discard((client_id, websocket))

    async def broadcast(self, message: dict, user_ids: list[int] | None = None):
        payload = {
            "message": message,
            "user_ids": user_ids,
        }

        await self.redis.publish(
            self.REDIS_CHANNEL,
            json.dumps(payload),
        )

    async def _redis_listener(self):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(self.REDIS_CHANNEL)
        try:
            async for item in pubsub.listen():
                if item["type"] != "message":
                    continue

                payload = json.loads(item["data"])
                await self._broadcast_local(
                    message=payload["message"],
                    user_ids=payload["user_ids"],
                )

        except asyncio.CancelledError:
            raise asyncio.CancelledError()

        finally:
            await pubsub.unsubscribe(self.REDIS_CHANNEL)
            await pubsub.close()

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
