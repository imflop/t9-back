import logging
import typing as t
from types import FrameType

from loguru import logger


class InterceptHandler(logging.Handler):  # type: ignore
    def emit(self, record: logging.LogRecord) -> None:  # type: ignore
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2  # type: ignore
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = t.cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )
