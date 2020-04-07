import redis
from fastapi import FastAPI
from loguru import logger
from redis import Redis

from app.core.config import REDIS_DB, REDIS_HOST, REDIS_PORT


class RedisConnectionPool(redis.ConnectionPool):
    def get_redis(self) -> redis.Redis:
        return redis.Redis(connection_pool=self)


def get_redis_connection() -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,)


async def connect_to_redis(app: FastAPI) -> None:
    if not getattr(app.state, "pool", None):
        logger.info(f"Connecting to {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

        app.state.pool = RedisConnectionPool(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
        )

        logger.info("Connection established")


async def close_redis_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    app.state.pool.disconnect()

    logger.info("Connection closed")
