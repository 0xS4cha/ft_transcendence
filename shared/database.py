from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class   Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "postgres"
    SCHEME: str = "postgresql+asyncpg"

    DEBUG: bool = False

    FRONTEND_URL: str = "https://localhost:8443"

    SECRET_JWT_KEY: str
    RIOT_API_KEY: str

    FORTYTWO_CLIENT_ID: str
    FORTYTWO_CLIENT_SECRET: str
    FORTYTWO_REDIRECT_URI: HttpUrl

    HOST_IP: str

    @property
    def database_url(self) -> str:
        return (str(
                PostgresDsn.build(
                    scheme = self.SCHEME,
                    username = self.POSTGRES_USER,
                    password = self.POSTGRES_PASSWORD,
                    host = self.POSTGRES_HOST,
                    port = self.POSTGRES_PORT,
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

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.async_session_factory() as async_session:
            yield async_session

    @asynccontextmanager
    async def lifespan(self, _app: FastAPI) -> AsyncGenerator[None]:
        yield
        await self.engine.dispose()

db = Database()
type AsyncSessionDep = Annotated[AsyncSession, Depends(db.get_async_session)]