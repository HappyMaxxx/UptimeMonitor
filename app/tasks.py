import httpx
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger

from app.database import db
from app.celery_app import celery_app

logger = get_task_logger(__name__)

@celery_app.task
def dispatcher_task():
    now = datetime.now()
    logger.info(f"{list(db.targets.values())}")
    targets_to_check = [target for target in list(db.targets.values()) if target.status in ['PENDING', 'UP', 'DOWN']]
    
    for target in targets_to_check:
        logger.info(f"Checking target {target.id} - {target.url} - Last checked at {target.updated_at} - Status: {target.status}")
        if target.updated_at + timedelta(minutes=target.check_interval) <= now:
            ping.delay(target.id)

@celery_app.task
def ping(target_id: int):
    target = db.get_target(target_id)
    if not target:
        return

    target.status = 'CHECKING'
    response = httpx.get(target.url)
    target.status = 'UP' if response.is_success() else 'DOWN'
    target.updated_at = datetime.now()

    return target.status