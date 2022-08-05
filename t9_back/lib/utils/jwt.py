import datetime as dt
import typing as t

import jwt
from pydantic import ValidationError

from ...lib.serializers.user import User
from ..domains.jwt import JWTMeta, JWTUser


JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week


def _create_jwt_token(*, jwt_content: t.Dict[str, t.Any], secret_key: str, expires_delta: dt.timedelta) -> str:
    to_encode = jwt_content.copy()
    expire = dt.datetime.now(dt.timezone.utc) + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return _create_jwt_token(
        jwt_content=JWTUser(email=user.email).dict(),
        secret_key=secret_key,
        expires_delta=dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def get_user_email_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).email
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
