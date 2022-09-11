from fastapi import Depends

from .repositories import link_repository_factory, stats_repository_factory, user_repository_factory
from ..dal.links import LinkRepository
from ..dal.stats import StatsRepository
from ..dal.users import UserRepository
from ..services.jwt import JWTService
from ..services.link import LinkService
from ..services.qr import QRService
from ..services.shorter import ShorterService
from ..services.user import UserService


def shorter_service_factory() -> ShorterService:
    return ShorterService()


def link_service_factory(
    link_repository: LinkRepository = Depends(link_repository_factory),
    stat_repository: StatsRepository = Depends(stats_repository_factory)
) -> LinkService:
    return LinkService(link_repository, stat_repository)


def user_service_factory(user_repository: UserRepository = Depends(user_repository_factory)) -> UserService:
    return UserService(user_repository)


def jwt_service_factory() -> JWTService:
    return JWTService()


def qr_service_factory() -> QRService:
    return QRService()
