import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend_app.core.jwt import Token
from backend_app.core.rate_limiter import ws_ratelimit
from backend_app.core.websocket import wsConnectionManager
from shared.database import AsyncSessionDep

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSessionDep):
    current_user = await Token.user_from_token(
        websocket.cookies.get("access_token"), session
    )
    await session.close()
    if current_user is None:
        await websocket.close(code=1008)
        return

    await wsConnectionManager.connect(websocket, current_user.id)
    try:
        while True:
            await websocket.receive_text()
            if not await ws_ratelimit(websocket, context_key=str(current_user.id)):
                await websocket.close(code=1008, reason="Rate limit exceeded")
                break
    except WebSocketDisconnect as e:
        logger.info(f"[websocket_endpoint] Websocket disconnected: {e}")
    finally:
        await wsConnectionManager.disconnect(websocket, current_user.id)
