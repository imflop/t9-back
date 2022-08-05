import logging
import sys
import typing as t

from loguru import logger
from pydantic import (
    BaseSettings,
    Field,
    PostgresDsn,
)

from .logging import InterceptHandler


SETTINGS_KEY: str = "settings"


class BaseAppSettings(BaseSettings):
    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    class Config:
        validate_assignment = True

    debug: bool = Field(False, env="debug", help="Debug flag")
    host: str = Field("0.0.0.0", env="host", help="Hostname to run webserver")
    port: int = Field(9000, env="port", help="Webservers port")
    sentry_dsn: t.Optional[str] = Field(None, env="sentry_dsn", help="Sentry DSN")

    database_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://fl:gfhjkm@localhost:5432/t9",
        env="database_dsn",
        help="Database DSN",
    )
    max_connection_count: int = 10
    min_connection_count: int = 10

    secret_key: str = "super-secret-key"

    allowed_hosts: t.Sequence[str] = ["*"]
    logging_level: int = logging.INFO  # type: ignore
    loggers: t.Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]  # type: ignore
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)  # type: ignore
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
