from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .base import async_session_factory
from ..dal.links import LinkRepository
from ..dal.stats import StatsRepository
from ..dal.users import UserRepository


def link_repository_factory(db: AsyncSession = Depends(async_session_factory)) -> LinkRepository:
    return LinkRepository(db)


def stats_repository_factory(db: AsyncSession = Depends(async_session_factory)) -> StatsRepository:
    return StatsRepository(db)


def user_repository_factory(db: AsyncSession = Depends(async_session_factory)) -> UserRepository:
    return UserRepository(db)
