
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend_app.core.jwt import Token
from backend_app.core.websocket import wsConnectionManager
from shared.database import AsyncSessionDep

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSessionDep):
    await websocket.accept()

    print("WEBSOCKET CONNECTED")

    try:
        while True:
            data = await websocket.receive_text()
            print("received:", data)
            await websocket.send_text(f"echo: {data}")
    except WebSocketDisconnect:
        print("WEBSOCKET DISCONNECTED")



    #token = websocket.cookies.get("access_token")
    #if not token:
    #    await websocket.close(code=1008)
    #    return

    #try:
    #    current_user = await Token.get_current_user(token, session)
    #except Exception: # noqa: BLE001
    #    await websocket.close(code=1008)
    #    return

    #await wsConnectionManager.connect(websocket, current_user.id)
    #try:
    #    while True:
    #        await websocket.receive_text()
    #except WebSocketDisconnect:
    #    await wsConnectionManager.disconnect(websocket, current_user.id)
