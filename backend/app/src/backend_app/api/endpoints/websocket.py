
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from shared.database import AsyncSessionDep
from backend_app.core.jwt import Token
from backend_app.core.websocket import wsConnectionManager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSessionDep):
    print("WEBSOCKET CONNECTED")
    print(websocket.cookies)

    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008)
        return
    try:
        current_user = await Token.get_current_user(token, session)
    except Exception: # noqa: BLE001
        await websocket.close(code=1008)
        return

    await wsConnectionManager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await wsConnectionManager.disconnect(websocket, current_user.id)
    print("WEBSOCKET DISCONNECTED")