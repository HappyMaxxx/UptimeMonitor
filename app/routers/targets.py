from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.targets import Target, TargetCreate, TargetResponse
from app.database import get_db
from app.models.targets import Target as TargetModel, TargetHistory
from app.tasks import ping

router = APIRouter()

@router.get('/targets', tags=['Targets'], response_model=List[TargetResponse])
def get_targets(db: Session = Depends(get_db)):
    targets = db.query(TargetModel).all()
    if not targets:
        raise HTTPException(status_code=404, detail="No targets found")
    return targets

@router.get('/targets/{id}/history', tags=['Targets'])
def get_target_history(id: int, db: Session = Depends(get_db),
                       limit: int = 10):
    
    query = (
        select(TargetHistory)
        .where(TargetHistory.target_id == id)
        .order_by(TargetHistory.created_at.desc())
        .limit(limit)
    )

    res = db.execute(query)

    if not res:
        raise HTTPException(status_code=404, detail="No target's history found")

    return res.scalars().all()

@router.post('/targets', tags=['Targets'], status_code=201, response_model=Target)
def create_target(target: TargetCreate, db: Session = Depends(get_db)):
    target_data = target.model_dump(mode="json")
    
    new_target = TargetModel(**target_data)

    history = TargetHistory(status=new_target.status)
    new_target.history.append(history)
    
    db.add(new_target)
    db.commit()
    db.refresh(new_target)

    ping.delay(new_target.id)

    return new_target

@router.delete('/targets/{id}', tags=['Targets'])
def delete_target(id: int, db: Session = Depends(get_db)):
    target = db.query(TargetModel).filter(TargetModel.id == id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    db.delete(target)
    db.commit()
    return None