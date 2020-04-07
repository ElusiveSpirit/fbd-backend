from celery import Celery

from app.core.config import CELERY_BROKER_URL, CELERY_RESULTS_BACKEND, TIMEZONE

app = Celery()

app.conf.update(
    timezone=TIMEZONE,
    broker_url=CELERY_BROKER_URL,
    results_backend=CELERY_RESULTS_BACKEND,
)

app.autodiscover_tasks(["app.servers", "app.guard"])
