from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy import delete

from backend_app.core.jwt import Token
from backend_app.models.chat_message import ChatMessage
from backend_app.models.friends import Friends
from backend_app.models.users import UserModel
from shared.database import AsyncSessionDep

router = APIRouter()

@router.delete("/me")
async def delete_account(
	current_user: Annotated[UserModel, Depends(Token.get_current_user)],
	session: AsyncSessionDep,
	response: Response
):
	user_id = current_user.id

	await session.execute(
		delete(ChatMessage).where(ChatMessage.owner_id == user_id)
	)
	await session.execute(
		delete(Friends).where(
			(Friends.uid1 == user_id) | (Friends.uid2 == user_id)
		)
	)
	await session.execute(
		delete(UserModel).where(UserModel.id == user_id)
	)
	await session.commit()

	return response.delete_cookie(
		key="access_token",
		path="/"
	)
