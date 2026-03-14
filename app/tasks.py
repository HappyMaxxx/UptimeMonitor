import time
import httpx
from fastapi import Depends
from datetime import datetime, timezone, timedelta
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.database import get_db, SessionLocal
from app.models.targets import Target as TargetModel
from app.models.targets import TargetHistory

logger = get_task_logger(__name__)

@celery_app.task
def dispatcher_task():
    now = datetime.now(timezone.utc)
    db_session = next(get_db())
    targets_to_check = [target for target in db_session.query(TargetModel).all() if target.status in ['PENDING', 'UP', 'DOWN']]
    
    for target in targets_to_check:
        if target.updated_at + timedelta(minutes=target.check_interval) <= now:
            ping.delay(target.id)

@celery_app.task(name="ping")
def ping(target_id: int):
    db = SessionLocal()
    try:
        target = db.query(TargetModel).filter(TargetModel.id == target_id).first()
        if not target:
            return f"Target {target_id} not found"

        start_time = time.time()
        try:
            response = httpx.get(target.url, timeout=10.0)
            duration = time.time() - start_time
            status = "UP" if response.status_code == 200 else "DOWN"
            code = response.status_code
        except Exception as e:
            duration = time.time() - start_time
            status = "DOWN"
            code = None

        target.status = status
        
        history = TargetHistory(
            target_id=target.id,
            status=status
        )
        db.add(history)
        db.commit()
        return f"Finished checking {target.url}: {status}"

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()