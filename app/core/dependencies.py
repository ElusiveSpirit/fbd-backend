from typing import AsyncGenerator, Callable, Type

from fastapi import Depends
from starlette.requests import Request

from app.core.repositories import BaseRepository
from app.db import RedisConnectionPool


def _get_redis_pool(request: Request) -> RedisConnectionPool:
    return request.app.state.pool


def get_repository(repo_type: Type[BaseRepository]) -> Callable:  # type: ignore
    async def _get_repo(
        pool: RedisConnectionPool = Depends(_get_redis_pool),
    ) -> AsyncGenerator[BaseRepository, None]:
        redis = pool.get_redis()
        yield repo_type(redis)

    return _get_repo
