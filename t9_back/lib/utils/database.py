from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import Session

from ..settings import AppSettings


def get_engine(settings: AppSettings) -> Session:
    engine = create_engine(settings.database_dsn)
    return Session(engine)


def get_async_engine(settings: AppSettings) -> AsyncEngine:
    return create_async_engine(settings.database_dsn, echo=bool(settings.debug))
