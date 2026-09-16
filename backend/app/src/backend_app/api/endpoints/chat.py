from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend_app.models.chat_message import ChatMessage
from backend_app.models.user import UserModel
from backend_app.core.jwt import Token 
from shared.database import AsyncSessionDep


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
    return {'success': True}