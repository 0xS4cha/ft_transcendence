import time
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, StringConstraints
from sqlalchemy import select

from backend_app.core.jwt import Token
from backend_app.core.websocket import WSbroadcast
from backend_app.models.chat_message import ChatMessage
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

MAX_MESSAGES_COUNT  = 200
MAX_MESSAGE_LENGTH  = 2000

class ChatMessageForm(BaseModel):
    content: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=MAX_MESSAGE_LENGTH),
    ]


def picture_url(picture: str | None) -> str | None:
    if not picture:
        return None
    if picture.startswith("https://"):
        return picture
    return f"/api/public/{picture}"

@router.post("/send")
async def send_chat(chat_message: ChatMessageForm, current_user: Annotated[UserModel, Depends(Token.get_current_user)], session: AsyncSessionDep):
    current_time = round(time.time() * 1000)
    message = ChatMessage(
        content=chat_message.content,
        date=current_time,
        owner=current_user
    )
    async with session:
        session.add(message)
        await session.commit()
    # broadcast message sent to all users
    data = {
        "id": message.id,
        "date": current_time,
        "content": chat_message.content,
        "user_id": current_user.id,
        "username": current_user.username,
        "picture": picture_url(current_user.picture),
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
            result = await session.execute(select(ChatMessage, UserModel.username, UserModel.picture, UserModel.id)
                                           .join(UserModel, UserModel.id == ChatMessage.owner_id)
                                           .order_by(ChatMessage.date.desc())
                                           .limit(MAX_MESSAGES_COUNT))
            cached_messages = [
                {
                    "id": message.id,
                    "date": message.date,
                    "content": message.content,
                    "user_id": user_id,
                    "username": username,
                    "picture": picture_url(picture),
                }
                for message, username, picture, user_id in [r for r in result][::-1]
            ]
        last_refresh_timestamp = current_time
    return cached_messages
