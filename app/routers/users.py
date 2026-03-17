from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.users import User
from app.schemas.auth import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse, tags=['Users'])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user