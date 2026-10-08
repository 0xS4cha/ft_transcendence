from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.models.users import UserModel


class Authenticate:
    @staticmethod
    async def get_user(
        user_email: str,
        session: AsyncSession,
    ) -> UserModel | None:
        return await session.scalar(
            select(UserModel).where(UserModel.email == user_email.strip().lower())
        )