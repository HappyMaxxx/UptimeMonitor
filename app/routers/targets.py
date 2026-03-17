from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.targets import Target, TargetCreate, TargetResponse
from app.database import get_db
from app.models.targets import Target as TargetModel, TargetHistory
from app.models.users import User
from app.dependencies import get_current_user
from app.tasks import ping

router = APIRouter()

@router.get('/targets', tags=['Targets'], response_model=List[TargetResponse])
def get_targets(db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)
                ):
    
    targets = db.query(TargetModel).filter(TargetModel.owner_id == current_user.id).all()
    if not targets:
        return []
    return targets

@router.get('/targets/{id}/history', tags=['Targets'])
def get_target_history(id: int,
                       db: Session = Depends(get_db),
                       limit: int = 10,
                       current_user: User = Depends(get_current_user)):
    
    target_exists = db.query(TargetModel).filter(
        TargetModel.id == id,
        TargetModel.owner_id == current_user.id
    ).first()

    if not target_exists:
        raise HTTPException(status_code=404, detail="Target not found or access denied")

    query = (
        select(TargetHistory)
        .where(TargetHistory.target_id == id)
        .order_by(TargetHistory.created_at.desc())
        .limit(limit)
    )

    res = db.execute(query)
    history_records = res.scalars().all()

    if not history_records:
        return []

    return history_records

@router.post('/targets', tags=['Targets'], status_code=201, response_model=TargetResponse)
def create_target(target: TargetCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    
    target_data = target.model_dump(mode="json")
    
    new_target = TargetModel(**target_data, owner_id=current_user.id)

    db.add(new_target)
    db.commit()
    db.refresh(new_target)
    
    ping.delay(new_target.id)
    return new_target

@router.delete('/targets/{id}', tags=['Targets'])
def delete_target(id: int,db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)
                  ):
    
    target = db.query(TargetModel).filter(
        TargetModel.id == id, 
        TargetModel.owner_id == current_user.id
    ).first()
    
    if not target:
        raise HTTPException(status_code=404, detail="Target not found or access denied")
        
    db.delete(target)
    db.commit()
    return {"message": "Deleted successfully"}