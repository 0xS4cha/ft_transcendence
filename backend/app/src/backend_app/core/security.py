from functools import lru_cache

from pwdlib import PasswordHash

from backend_app.core.authenticate import Authenticate
from shared.database import AsyncSessionDep
from backend_app.models.user import UserModel


class   Password:
    password_hash = PasswordHash.recommended()
    dummy_password = "@FnN7m+ZuAqg"

    @staticmethod
    def hash_password(
            password: str
    ) -> str:
        return Password.password_hash.hash(password)

    @staticmethod
    def verify_password(
            plain_password: str,
            hashed_password: str
    ) -> bool:
        return Password.password_hash.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    @lru_cache
    def get_dummy_hash() -> str:
        return Password.hash_password(Password.dummy_password)

    @staticmethod
    async def authenticate_user(
        username: str,
        password: str,
        session: AsyncSessionDep
    ) -> UserModel:

        user = await Authenticate.get_user(username, session)

        dummy_hash = Password.get_dummy_hash()

        if not user:
            Password.verify_password(password, dummy_hash)
            return False

        if not Password.verify_password(password, user.hashed_password):
            return False

        return user