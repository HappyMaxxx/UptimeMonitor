from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (HTTPBearer, HTTPAuthorizationCredentials, 
                              OAuth2PasswordBearer, OAuth2PasswordRequestForm)
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserResponse, Token, LoginRequest
from app.repositories.user_repo import UserRepository
from app.security import (
    verify_password, create_access_token, create_refresh_token, decode_token, authenticate
)

router = APIRouter()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=201, tags=['Auth'])
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    
    if repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username вже зайнятий")
    if repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email вже зареєстровано")
    
    user = repo.create(user_data)
    return user

@router.post("/login", response_model=Token, tags=['Auth'])
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_username(credentials.username)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний username або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Акаунт деактивовано")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=Token, tags=['Auth'])
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    payload = decode_token(credentials.credentials)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Невалідний refresh токен")
    
    user_id = int(payload.get("sub"))
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    
    new_access = create_access_token({"sub": str(user.id)})
    new_refresh = create_refresh_token({"sub": str(user.id)})
    
    return Token(access_token=new_access, refresh_token=new_refresh)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@router.post("/token", response_model=Token, tags=['Auth'])
def login_oauth2(form_data: OAuth2PasswordRequestForm = Depends(),
                 db: Session = Depends(get_db)):

    user = authenticate(db, form_data.username, form_data.password) 
    
    if not user:
        raise HTTPException(status_code=401, detail="Невірні дані")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }