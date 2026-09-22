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
        disconnected = []
        async def send(websocket: WebSocket, user_id: int):
            try:
                await websocket.send_json(message)
            except Exception: # noqa: BLE001
                disconnected.append((user_id, websocket))
        await asyncio.gather(*(send(ws, user_id) for user_id, ws in connections if user_id in (user_ids or [k for k, _ in connections])))
        for user_id, websocket in disconnected:
            await self.disconnect(websocket, user_id)


wsConnectionManager = WebsocketConnectionManager()

async def WSbroadcast(type: str, data: dict) -> int:
    await wsConnectionManager.broadcast({
        "type": type,
        "data": data,
    })
    return len(wsConnectionManager.connections) # total active connections

async def WSbroadcastToClientList(type: str, data: dict, user_ids: list[int]) -> int:
    for client_id in user_ids:
        await wsConnectionManager.broadcast({
            "type": type,
            "data": data,
        })
    return len(user_ids) # total active connections