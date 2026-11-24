from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connect import get_db
from db import crud
from dependencies import get_current_user, require_admin
import schemas

from dependencies import get_recommender

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=list[schemas.ArticleOut])
def list_articles(db: Session = Depends(get_db)):
    return crud.get_all_articles(db)

# ВАЖНО: /tag/{tag_id} должен идти ВЫШЕ /{article_id}
@router.get("/tag/{tag_id}", response_model=list[schemas.ArticleOut])
def articles_by_tag(tag_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_articles_by_tag(db, tag_id)
    except LookupError as e:
        raise HTTPException(404, str(e))

@router.get("/{article_id}", response_model=schemas.ArticleDetailWithRecommendationsOut)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    recommender = Depends(get_recommender), # Внедрение зависимости!
):
    try:
        article = crud.get_article_by_id(db, article_id)
    except (ValueError, LookupError) as e:
        raise HTTPException(404, str(e))

    # Вызов gRPC!
    similar = recommender(article_id, limit=5)

    return schemas.ArticleDetailWithRecommendationsOut(
        article_id=article.article_id,
        author_id=article.author_id,
        article_title=article.article_title,
        content=article.content,
        created_time=article.created_time,
        tags=[schemas.TagOut.model_validate(t) for t in article.tags],
        similar_articles=similar,
    )

@router.post("/", response_model=schemas.ArticleOut, status_code=201)
def create_article(data: schemas.ArticleCreate, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.create_article(db, data.article_title, data.content, author_id=admin.user_id)
    except LookupError as e:
        raise HTTPException(404, str(e))
    except PermissionError as e:
        raise HTTPException(403, str(e))

@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(article_id: int, data: schemas.ArticleUpdate,
                   db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return crud.update_article(db, article_id, data.article_title, data.content)
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        return {"message": crud.delete_article(db, article_id)}
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/{article_id}/likes", response_model=list[schemas.UserOut])
def article_likes(article_id: int, db: Session = Depends(get_db)):
    try:
        return crud.m2m_relationships.get_article_likes(db, article_id)
    except (ValueError, LookupError) as e:
        raise HTTPException(404, str(e))