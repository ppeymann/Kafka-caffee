from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from core.database import get_db
from models.auth import User
from repository.auth import AuthRepository
from schemas.auth import Token, UserCreate, UserSchema
from service.auth import AuthService, get_auth_service
from starlette import status
from utils.utils import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])


user_dependency = Annotated[dict, Depends(get_auth_service)]


@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    service = AuthService(repo)
    token = service.create_user(data)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return token

@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    repo = AuthRepository(db)
    service = AuthService(repo)
    token = service.login(data)
    if not token:
        raise HTTPException(status_code=401, detail="permission denied")

    return token

@router.get("/me", response_model=UserSchema)
def me(token: str = Depends(oauth2_scheme), service: AuthService = Depends(get_auth_service)):
    user = service.me(token)
    if not user:
        raise HTTPException(status_code=401, detail="permission denied")
    return user