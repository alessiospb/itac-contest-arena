from contextlib import asynccontextmanager
from enum import Enum
import allure
class LogLevel(Enum):
    INFO = "info"
    DEBUG = "debug"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@asynccontextmanager
async def log_message(logger, message: str, level: LogLevel, attach_to_allure: bool = True, space_number = 0):
    msg = " " * space_number + message
    if level == LogLevel.INFO:
        logger.info(msg)
    elif level == LogLevel.DEBUG:
        logger.debug(msg)
    elif level == LogLevel.WARNING:
        logger.warning(msg)
    elif level == LogLevel.ERROR:
        logger.error(msg)
    elif level == LogLevel.CRITICAL:
        logger.critical(msg)

    if attach_to_allure:
        with allure.step(msg):
            yield
    else:
        yield

