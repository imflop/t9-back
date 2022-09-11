from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from ...lib.errors import EntityDoesNotExist
from ...lib.factories.base import settings_factory
from ...lib.factories.services import (
    jwt_service_factory,
    user_service_factory,
)
from ...lib.serializers.user import User, UserIn
from ...lib.services.jwt import JWTService
from ...lib.services.user import UserService
from ...lib.settings import AppSettings


router = APIRouter()


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    new_user: UserIn,
    user_service: UserService = Depends(user_service_factory),
    jwt_service: JWTService = Depends(jwt_service_factory),
    settings: AppSettings = Depends(settings_factory),
) -> User:
    if await user_service.is_email_taken(new_user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = await user_service.create_user(new_user)
    user.token = jwt_service.create_access_token_for_user(user, settings.secret_key)

    return user


@router.post(
    "/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_login: UserIn,
    user_service: UserService = Depends(user_service_factory),
    jwt_service: JWTService = Depends(jwt_service_factory),
    settings: AppSettings = Depends(settings_factory),
) -> User:
    wrong_email_or_password = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect login or password",
    )

    try:
        user = await user_service.get_user(user_login.email)
    except EntityDoesNotExist as e:
        raise wrong_email_or_password from e

    if not user.check_password(user_login.password):
        raise wrong_email_or_password

    user.token = jwt_service.create_access_token_for_user(user, settings.secret_key)

    return user
