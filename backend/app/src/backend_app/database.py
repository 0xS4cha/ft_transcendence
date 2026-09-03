from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

class   Base(DeclarativeBase):
    pass

class   Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "postgres"
    DEBUG_HOST: str = "localhost"
    SCHEME: str = "postgresql+asyncpg"
    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        return (str(
                PostgresDsn.build(
                    scheme = self.SCHEME,
                    username = self.POSTGRES_USER,
                    password = self.POSTGRES_PASSWORD,
                    host = self.DEBUG_HOST if self.DEBUG else self.POSTGRES_HOST,
                    port = self.PORT,
                    path = self.POSTGRES_DB
                )
            )
        )

class   Database:
    def __init__(self):
        self.settings = Settings()
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.DEBUG
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )
        self.async_session_dep = Annotated[AsyncSession, Depends(self.get_async_session)]

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as async_session:
            yield async_session

    async def close(self) -> None:
        await self.engine.dispose()

db = Database()

print(f"\n\033[1;35mDATABASE_URL: \033[0;35m{db.settings.database_url}\033[0m\n")

@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
