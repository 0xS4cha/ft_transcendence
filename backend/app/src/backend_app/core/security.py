from functools import lru_cache

from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from backend_app.core.authenticate import Authenticate
from backend_app.models.users import UserModel


class Password:
    password_hash = PasswordHash.recommended()
    dummy_password = "@FnN7m+ZuAqg"

    @staticmethod
    def hash_password(password: str) -> str:
        return Password.password_hash.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Password.password_hash.verify(plain_password, hashed_password)

    @staticmethod
    @lru_cache
    def get_dummy_hash() -> str:
        return Password.hash_password(Password.dummy_password)

    @staticmethod
    async def authenticate_user(
        email: str,
        password: str,
        session: AsyncSession,
    ) -> UserModel | None:
        user = await Authenticate.get_user(email, session)

        if user is None:
            Password.verify_password(password, Password.get_dummy_hash())
            return None

        if not Password.verify_password(password, user.hashed_password):
            return None

        return user