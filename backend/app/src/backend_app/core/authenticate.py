from sqlalchemy import func, select
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

    @staticmethod
    async def username_taken(
        username: str,
        session: AsyncSession,
        exclude_user_id: int | None = None,
    ) -> bool:
        query = select(UserModel.id).where(
            func.lower(UserModel.username) == username.lower()
        )
        if exclude_user_id is not None:
            query = query.where(UserModel.id != exclude_user_id)
        return await session.scalar(query) is not None
