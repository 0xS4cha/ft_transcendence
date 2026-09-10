from sqlalchemy import select

from shared.database import AsyncSessionDep
from backend_app.models.user import UserModel


class Authenticate:
    @staticmethod
    async def get_user(
        user_email: str,    
        session: AsyncSessionDep
    ) -> UserModel:
        existing_user = await session.scalar(
                select(UserModel).where(UserModel.email == user_email)
        )
        
        if not existing_user:
            return (False)
        
        return (existing_user)