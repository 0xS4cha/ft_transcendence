from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from backend_app.models.user import UserModel
from backend_app.core.jwt import Token 
from shared.datebase import AsyncSessionDep


router = APIRouter()

class ChatMessage(BaseModel):
    content: str | None = None

@router.post("/send")
def send_chat(chat_message: ChatMessage, current_user: Annotated[UserModel, Depends(Token.get_current_user)]):
    if not chat_message.content:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    current_date = datetime.now(UTC).date()
    