from celery.task import Task
from loguru import logger

from app.celery import app
from app.core.repositories import EntityDoesNotExist
from app.db import get_redis_connection
from app.severs.repositories import ServerIsBusy, ServersRepository
from app.severs.services import clean_server


@app.task(bind=True, default_retry_delay=5 * 60, retry_kwargs={"max_retries": 3})
def clean_server_task(self: Task, server_slug: str) -> None:
    redis = get_redis_connection()
    servers_repository = ServersRepository(redis)
    try:
        clean_server(servers_repository, server_slug)
    except ServerIsBusy as exc:
        logger.warning(f"Could not clean {server_slug} server. Server is busy.")
        self.retry(exc=exc)
    except EntityDoesNotExist:
        logger.warning(f"Could not clean {server_slug} server. Not found error.")


@app.task
def check_mr_status_task(server_slug: str) -> None:
    raise NotImplementedError
