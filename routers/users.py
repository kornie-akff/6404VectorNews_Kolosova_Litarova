from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from dependencies import require_admin, get_current_user
import schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), admin = Depends(require_admin)):
    return crud.get_all_users(db)

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.get_user_by_id(db, user_id)
    except LookupError as e:
        raise HTTPException(404, str(e))

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    if not (current_user.user_id == user_id):
        raise HTTPException(403, "Можно редактировать только свой профиль")
    
    try:
        return crud.update_user(
            db, user_id,
            new_username=data.username,
            new_email=data.email,
            new_password=data.password,
        )
    except LookupError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{user_id}/likes", response_model=list[schemas.ArticleOut])
def user_likes(user_id: int, db: Session = Depends(get_db)):
    try:
        return crud.m2m_relationships.get_user_likes(db, user_id)
    except LookupError as e:
        raise HTTPException(404, str(e))

@router.delete("/{user_id}")
def deactivate(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    is_admin = current_user.role.role_name == "admin"
    is_self = current_user.user_id == user_id

    if not is_admin and not is_self:
        raise HTTPException(403, "Можно деактивировать только свой профиль (или нужна роль admin)")

    try:
        crud.deactive_user(db, user_id)
        return {"message": "Пользователь деактивирован"}
    except LookupError as e:
        raise HTTPException(404, str(e))