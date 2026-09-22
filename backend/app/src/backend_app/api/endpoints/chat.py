import time
from datetime import UTC, datetime
from typing import Annotated

import ciso8601
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.core.websocket import WSbroadcast
from backend_app.models.chat_message import ChatMessage
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

class ChatMessageForm(BaseModel):
    content: str | None = None

@router.post("/send")
async def send_chat(chat_message: ChatMessageForm, current_user: Annotated[UserModel, Depends(Token.get_current_user)], session: AsyncSessionDep):
    if not chat_message.content:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not send empty message"
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
    data = {
        "id": current_user.id,
        "date": ciso8601.parse_datetime(current_date),
        "content": chat_message.content,
        "username": current_user.username,
        "picture": current_user.picture,
    }
    await WSbroadcast("chat.msg", data)
    return data

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
            result = await session.execute(select(ChatMessage, UserModel.username, UserModel.picture).join(UserModel, UserModel.id == ChatMessage.owner_id))
            cached_messages = [
                {
                    "id": message.id,
                    "date": ciso8601.parse_datetime(message.date),
                    "content": message.content,
                    "username": username,
                    "picture": picture
                }
                for message, username, picture in result
            ]
        last_refresh_timestamp = current_time
    return cached_messages
