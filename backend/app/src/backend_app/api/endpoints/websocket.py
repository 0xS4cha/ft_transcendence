from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Cookie

from backend_app.core.jwt import Token
from backend_app.core.websocket import wsConnectionManager
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSessionDep):
    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        current_user = await Token.get_current_user(token, session)
    except Exception:
        await websocket.close(code=1008)
        return

    await wsConnectionManager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await wsConnectionManager.disconnect(websocket, current_user.id)
