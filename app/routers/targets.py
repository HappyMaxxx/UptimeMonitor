from typing import List
from celery.schedules import crontab
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.schemas.targets import Target, TargetCreate, TargetResponse
from app.database import get_db
from app.celery_app import celery_app
from app.models.targets import Target as TargetModel

router = APIRouter()

@router.get('/targets', tags=['Targets'], response_model=List[TargetResponse])
def get_targets(db: Session = Depends(get_db)):
    targets = db.query(TargetModel).all()
    if not targets:
        raise HTTPException(status_code=404, detail="No targets found")
    return targets

@router.get('/targets/{id}/history', tags=['Targets'])
def get_target_history(id: int):
    # TODO: Implement history retrieval logic
    pass

@router.post('/targets', tags=['Targets'], status_code=201, response_model=Target)
def create_target(target: TargetCreate, background_tasks: BackgroundTasks,
                  db: Session = Depends(get_db)):
    target_data = target.model_dump(mode="json")
    new_target = TargetModel(**target_data)
    db.add(new_target)
    db.commit()
    db.refresh(new_target)

    return new_target

@router.delete('/targets/{id}', tags=['Targets'])
def delete_target(id: int, db: Session = Depends(get_db)):
    target = db.query(TargetModel).filter(TargetModel.id == id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    db.delete(target)
    db.commit()
    return None