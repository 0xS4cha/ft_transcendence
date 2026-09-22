from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from backend_app.core.jwt import Token
from backend_app.core.websocket import wsConnectionManager
from backend_app.models.users import UserModel

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, current_user: Annotated[UserModel, Depends(Token.get_current_user)]):
    await wsConnectionManager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await wsConnectionManager.disconnect(websocket, current_user.id)
