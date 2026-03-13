import httpx

from datetime import datetime, timezone, timedelta
from celery.utils.log import get_task_logger

from app.celery_app import celery_app
from app.database import get_db
from app.models.targets import Target as TargetModel

logger = get_task_logger(__name__)

@celery_app.task
def dispatcher_task():
    now = datetime.now(timezone.utc)
    db_session = next(get_db())
    targets_to_check = [target for target in db_session.query(TargetModel).all() if target.status in ['PENDING', 'UP', 'DOWN']]
    
    for target in targets_to_check:
        logger.info(f"Checking target {target.id} - {target.url} - Last checked at {target.updated_at} - Status: {target.status}")
        if target.updated_at + timedelta(minutes=target.check_interval) <= now:
            ping.delay(target.id)

@celery_app.task
def ping(target_id: int):
    db_session = next(get_db())
    target = db_session.query(TargetModel).filter(TargetModel.id == target_id).first()
    if not target:
        return

    try:
        response = httpx.get(target.url, timeout=10)
        target.status = 'UP' if response.status_code == 200 else 'DOWN'
    except Exception as e:
        target.status = 'DOWN'
    finally:
        target.updated_at = datetime.now()
        db_session.commit()
        db_session.refresh(target)

    return target.status