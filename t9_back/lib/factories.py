import typing as t

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .dal.links import LinkRepository
from .dal.users import UserRepository
from .dal.stats import StatsRepository
from .services.jwt import JWTService
from .services.link import LinkService
from .services.qr import QRService
from .services.shorter import ShorterService
from .services.user import UserService
from .settings import SETTINGS_KEY, AppSettings
from .utils.database import get_async_engine


def settings_factory(request: Request) -> AppSettings:
    return request.app.extra[SETTINGS_KEY]


async def db_factory(settings: AppSettings = Depends(settings_factory)) -> t.AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(get_async_engine(settings), class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


def shorter_service_factory() -> ShorterService:
    return ShorterService()


def link_repository_factory(db: AsyncSession = Depends(db_factory)) -> LinkRepository:
    return LinkRepository(db)


def stats_repository_factory(db: AsyncSession = Depends(db_factory)) -> StatsRepository:
    return StatsRepository(db)


def link_service_factory(
    link_repository: LinkRepository = Depends(link_repository_factory),
    stat_repository: StatsRepository = Depends(stats_repository_factory)
) -> LinkService:
    return LinkService(link_repository, stat_repository)


def user_repository_factory(db: AsyncSession = Depends(db_factory)) -> UserRepository:
    return UserRepository(db)


def user_service_factory(user_repository: UserRepository = Depends(user_repository_factory)) -> UserService:
    return UserService(user_repository)


def jwt_service_factory() -> JWTService:
    return JWTService()


def qr_service_factory() -> QRService:
    return QRService()
