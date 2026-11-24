# dependencies.py
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from grpc_service.client import get_similar_articles

def get_current_user(
    x_user_id: int = Header(..., description="ID текущего пользователя"),
    db: Session = Depends(get_db),
):
    """
    аутентификация:
    клиент передаёт заголовок X-User-Id: <user_id>.
    """
    try:
        user = crud.get_user_by_id(db, x_user_id)
    except LookupError as e:
        raise HTTPException(status_code=401, detail=str(e))

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь деактивирован")

    return user


def require_admin(user=Depends(get_current_user)):
    """Проверка роли admin. Используется как зависимость в эндпоинтах."""
    if user.role.role_name != "admin":
        raise HTTPException(status_code=403, detail="Требуется роль admin")
    return user


def get_recommender():
    """FastAPI-зависимость: клиент gRPC-сервиса рекомендаций."""
    return get_similar_articles