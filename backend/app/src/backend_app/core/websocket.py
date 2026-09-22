import asyncio

from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.connections: set[tuple[int, WebSocket]] = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        async with self.lock:
            self.connections.add((client_id, websocket))

    async def disconnect(self, websocket: WebSocket, client_id: int):
        async with self.lock:
            self.connections.discard((client_id, websocket))

    async def broadcast(self, message: dict, user_ids: list[int] | None = None):
        async with self.lock:
            connections = list(self.connections)

        if user_ids is not None:
            connections = [
                (user_id, ws)
                for user_id, ws in connections
                if user_id in user_ids
            ]

        async def send(user_id: int, websocket: WebSocket):
            try:
                await websocket.send_json(message)
            except Exception: # noqa: BLE001
                await self.disconnect(websocket, user_id)

        await asyncio.gather(*(send(user_id, websocket) for user_id, websocket in connections))


wsConnectionManager = WebsocketConnectionManager()

async def WSbroadcast(type: str, data: dict, user_ids: list[int] | None = None,) -> int:
    print("CONNECTIONS:", len(wsConnectionManager.connections))
    print("CONNECTIONS DATA:", wsConnectionManager.connections)
    await wsConnectionManager.broadcast(
        {
            "type": type,
            "data": data,
        },
        user_ids
    )
    if user_ids is not None:
        return len(user_ids)
    return len(wsConnectionManager.connections)
