import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from app.core.logging import InterceptHandler

PROJECT_NAME = "FBD project"
VERSION = "0.0.1"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

REDIS_HOST: str = config("REDIS_HOST", default="redis")
REDIS_PORT: int = config("REDIS_PORT", cast=int, default=6379)  # noqa: WPS432
REDIS_DB: int = config("REDIS_DB", cast=int, default=0)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

TIMEZONE: str = "Europe/Moscow"

DEFAULT_ACCESS_CLOSE_TIMEOUT = 60  # in minutes

# celery configuration

CELERY_BROKER_URL: str = config("CELERY_BROKER_URL", default="redis://localhost:6379/1")
CELERY_RESULTS_BACKEND: str = config(
    "CELERY_RESULTS_BACKEND", default="redis://localhost:6379/2"
)

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
