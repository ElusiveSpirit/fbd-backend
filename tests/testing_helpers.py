import re
from typing import List, Optional


class FakeRedis:
    def __init__(self) -> None:
        self.db = {}

    def set(self, key: str, value: str) -> None:
        self.db[key] = value

    def get(self, key: str) -> Optional[str]:
        return self.db.get(key)

    def keys(self, pattern: str) -> List[str]:
        return [key for key in self.db.keys() if re.match(pattern, key)]

    def delete(self, key: str) -> None:
        del self.db[key]


class FakeRedisConnectionPool:
    def __init__(self) -> None:
        self.__redis = None

    def get_redis(self) -> FakeRedis:
        if self.__redis is None:
            self.__redis = FakeRedis()
        return self.__redis

    def disconnect(self) -> None:
        """Fake disconnect"""
