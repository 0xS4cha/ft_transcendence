import asyncio

from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, int client_id):
        await websocket.accept()
        async with self.lock:
            self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            self.connections.discard(websocket)

    async def broadcast(self, message: dict):
        async with self.lock:
            connections = list(self.connections)
        disconnected = []
        async def send(websocket: WebSocket):
            try:
                await websocket.send_json(message)
            except Exception: # noqa: BLE001
                disconnected.append(websocket)
        await asyncio.gather(*(send(ws) for ws in connections))
        for websocket in disconnected:
            await self.disconnect(websocket)


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