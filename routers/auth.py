from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from db.security import verify_password
import schemas

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, data.username, data.email, data.password, role_id=2)  # reader
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=schemas.LoginResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, data.username)   # см. п.4
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Неверный логин или пароль")
    if not user.is_active:
        raise HTTPException(403, "Пользователь деактивирован")
    return schemas.LoginResponse(
        user_id=user.user_id, username=user.username,
        role_id=user.role_id, message="Успешный вход",
    )