from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "worker",
    broker_url=settings.celery_broker_url,
    result_backend=settings.celery_result_backend,
    include=["app.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

celery_app.conf.beat_schedule = {
    "check-targets-every-minute": {
        "task": "app.tasks.dispatcher_task",
        "schedule": crontab(minute="*"),
    },
}

celery_app.conf.beat_scheduler = "celery.beat:PersistentScheduler"
celery_app.conf.beat_schedule_filename = "/tmp/celerybeat-schedule"