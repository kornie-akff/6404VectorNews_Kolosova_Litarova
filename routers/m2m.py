from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from dependencies import get_current_user, require_admin
import schemas

router = APIRouter(prefix="/actions", tags=["m2m"])

# ==== теги статьи ====
@router.post("/articles/{article_id}/tags/{tag_id}", response_model=schemas.ArticleDetailOut)
def add_tag(article_id: int, tag_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.add_tag_to_article(db, article_id, tag_id)
    except LookupError as e:
        raise HTTPException(404, str(e))

@router.delete("/articles/{article_id}/tags/{tag_id}", response_model=schemas.ArticleDetailOut)
def remove_tag(article_id: int, tag_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.remove_tag_from_article(db, article_id, tag_id)
    except LookupError as e:
        raise HTTPException(404, str(e))

# ==== лайки ====
@router.post("/articles/{article_id}/like")
def like(article_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        crud.like_article(db, user.user_id, article_id)
        return {"message": "Лайк поставлен"}
    except (ValueError, LookupError) as e:
        raise HTTPException(404, str(e))

@router.delete("/articles/{article_id}/like")
def unlike(article_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        crud.unlike_article(db, user.user_id, article_id)
        return {"message": "Лайк убран"}
    except (ValueError, LookupError) as e:
        raise HTTPException(404, str(e))

# ==== подписки ====
@router.post("/tags/{tag_id}/subscribe")
def subscribe(tag_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        crud.subscribe_to_tag(db, user.user_id, tag_id)
        return {"message": "Подписка оформлена"}
    except LookupError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(409, str(e))

@router.delete("/tags/{tag_id}/subscribe")
def unsubscribe(tag_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        return {"message": crud.unsubscribe_from_tag(db, user.user_id, tag_id)}
    except LookupError as e:
        raise HTTPException(404, str(e))

@router.get("/me/subscriptions", response_model=list[schemas.TagSubscriptionOut])
def my_subscriptions(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return crud.get_user_subscriptions(db, user.user_id)

@router.patch("/tags/{tag_id}/notifications")
def set_notif(tag_id: int, data: schemas.NotificationSettingUpdate,
              db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        crud.set_notification(db, user.user_id, tag_id, data.enabled)
        return {"message": "Настройки обновлены"}
    except LookupError as e:
        raise HTTPException(404, str(e))