from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.db import close_redis_connection, connect_to_redis


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_redis(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_redis_connection(app)

    return stop_app
