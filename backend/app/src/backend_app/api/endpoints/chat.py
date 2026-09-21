import time
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.models.chat_message import ChatMessage
from backend_app.models.user import UserModel
from shared.database import AsyncSessionDep
from backend_app.core.websocket import WSbroadcast

router = APIRouter()

class ChatMessageForm(BaseModel):
    content: str | None = None

@router.post("/send")
async def send_chat(chat_message: ChatMessageForm, current_user: Annotated[UserModel, Depends(Token.get_current_user)], session: AsyncSessionDep):
    if not chat_message.content:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    current_date = datetime.now(UTC).date()
    async with session:
        session.add(ChatMessage(
            content=chat_message.content,
            date=current_date,
            owner=current_user
		))
        await session.commit()
    # broadcast message sent to all users
    await WSbroadcast("chat.msg", {"author_id": current_user.id, "author_name": current_user.username, "message": chat_message.content, "date": current_date})
    return {'success': True}

cached_messages = []
last_refresh_timestamp = 0
refresh_delta_s = 2
@router.get("/messages")
async def messages(current_user: Annotated[UserModel, Depends(Token.get_current_user)], session: AsyncSessionDep):
    global cached_messages
    global last_refresh_timestamp

    current_time = time.time()
    if current_time - last_refresh_timestamp > refresh_delta_s:
        async with session:
            result = await session.execute(select(ChatMessage, UserModel.username).join(UserModel, UserModel.id == ChatMessage.owner_id))
            cached_messages = [
                {
                    "id": message.id,
                    "date": message.date,
                    "content": message.content,
                    "username": username,
                }
                for message, username in result
            ]
        last_refresh_timestamp = current_time
    return cached_messages
