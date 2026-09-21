from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend_app.core.websocket import wsConnectionManager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await wsConnectionManager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await wsConnectionManager.disconnect(websocket)
