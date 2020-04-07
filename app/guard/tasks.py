from datetime import datetime, timedelta

from app.celery import app
from app.core.config import DEFAULT_ACCESS_CLOSE_TIMEOUT
from app.db import get_redis_connection
from app.guard.repositories import GuardRepository
from app.guard.services import close_public_access, open_public_access


@app.task
def close_public_access_task() -> None:
    redis = get_redis_connection()
    guard_repository = GuardRepository(redis)
    close_public_access(guard_repository)


@app.task
def open_public_access_task() -> None:
    redis = get_redis_connection()
    guard_repository = GuardRepository(redis)
    open_public_access(guard_repository)
    close_public_access_task.apply_async(
        eta=datetime.now() + timedelta(minutes=DEFAULT_ACCESS_CLOSE_TIMEOUT)
    )
