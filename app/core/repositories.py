from typing import Any, AnyStr, Callable, Dict, List, Optional

import ujson
from redis import Redis


class RepositoryException(Exception):
    """Base repository exception"""


class EntityDoesNotExist(RepositoryException):
    """Raised when entity was not found in database."""


class BaseRepository:
    # Redis key prefix
    redis_prefix: Optional[str] = None
    dumps: Callable[..., str] = ujson.dumps
    loads: Callable[[AnyStr, bool], Any] = ujson.loads

    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        if self.redis_prefix is None:
            raise NotImplementedError("Must override prefix attr")

    @property
    def redis(self) -> Redis:
        return self._redis

    def get_redis_key_by_slug(self, slug: str) -> str:
        return f"{self.redis_prefix}:{slug}"

    def _save(self, key: str, saving_data: Dict[str, Any]) -> None:
        string_obj = self.dumps(saving_data)
        self.redis.set(key, string_obj)

    def _get(self, key: str) -> Optional[Dict[str, Any]]:
        string_obj = self.redis.get(key)
        return self.loads(string_obj) if string_obj else None

    def _get_list(self) -> List[Dict[str, Any]]:
        pattern = self.get_redis_key_by_slug("*")

        result_list = []
        for key in self.redis.keys(pattern):
            item_by_key = self._get(key)
            if item_by_key:
                result_list.append(item_by_key)
        return result_list

    def _delete(self, key: str) -> None:
        self.redis.delete(key)
