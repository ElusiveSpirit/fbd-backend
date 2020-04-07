from app.core.repositories import BaseRepository


class GuardRepository(BaseRepository):
    redis_prefix = "guard"

    opened_key = "opened"

    def get_opened(self) -> bool:
        key = self.get_redis_key_by_slug(self.opened_key)
        opened_status = self._get(key)
        return opened_status["opened"] if opened_status else False

    def set_opened(self, *, opened: bool) -> None:
        key = self.get_redis_key_by_slug(self.opened_key)
        self._save(key, {"opened": opened})
