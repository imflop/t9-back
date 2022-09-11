import typing as t

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from ..settings import AppSettings, SETTINGS_KEY


def settings_factory(request: Request) -> AppSettings:
    return request.app.extra[SETTINGS_KEY]


def get_async_engine(settings: AppSettings) -> AsyncEngine:
    return create_async_engine(settings.database_dsn, echo=bool(settings.debug))


async def async_session_factory(
    settings: AppSettings = Depends(settings_factory)
) -> t.AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(get_async_engine(settings), class_=AsyncSession, expire_on_commit=False, future=True)

    async with async_session() as session:
        yield session
