from typing import List
from celery.schedules import crontab
from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas.targets import Target, TargetCreate, TargetResponse
from app.database import db
from app.celery_app import celery_app

router = APIRouter()

@router.get('/targets', tags=['Targets'], response_model=List[TargetResponse])
def get_targets():
    if not db.targets:
        raise HTTPException(status_code=404, detail="No targets found")
    return list(db.targets.values())

@router.get('/targets/{id}/history', tags=['Targets'])
def get_target_history(id: int):
    # TODO: Implement history retrieval logic
    pass

@router.post('/targets', tags=['Targets'], status_code=201, response_model=Target)
def create_target(target: TargetCreate, background_tasks: BackgroundTasks):
    new_target_data = target.model_dump()
    new_target_data['id'] = db.counter.get_next()
    new_target = Target(**new_target_data)
    db.targets[new_target_data['id']] = new_target

    background_tasks.add_task(celery_app.send_task, 'app.tasks.ping', [new_target.id])

    return new_target

@router.delete('/targets/{id}', tags=['Targets'])
def delete_target(id: int):
    if id not in db.targets:
        raise HTTPException(status_code=404, detail="Target not found")
    del db.targets[id]
    return None