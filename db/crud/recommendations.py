from sqlalchemy.orm import Session
from sqlalchemy import select, func
from db.models import Article, User
from db.models.associations import likes


def get_similar_articles(session: Session, article_id: int, limit: int = 5) -> list[dict]:
    """
    Коллаборативная фильтрация по лайкам:
    статьи, которые лайкали те же пользователи, что и article_id,
    отсортированные по числу общих лайкеров.
    """
    # пользователи, лайкнувшие исходную статью
    likers_subq = (
        select(likes.c.user_id)
        .where(likes.c.article_id == article_id)
        .subquery()
    )

    # статьи, лайкнутые этими пользователями, кроме самой исходной
    stmt = (
        select(
            Article.article_id,
            Article.article_title,
            Article.author_id,
            func.count(likes.c.user_id).label("common_likers"),
        )
        .join(likes, likes.c.article_id == Article.article_id)
        .where(
            likes.c.user_id.in_(select(likers_subq.c.user_id)),
            Article.article_id != article_id,
        )
        .group_by(Article.article_id, Article.article_title, Article.author_id)
        .order_by(func.count(likes.c.user_id).desc(), Article.created_time.desc())
        .limit(limit)
    )
    rows = session.execute(stmt).all()
    return [
        {
            "article_id": r.article_id,
            "article_title": r.article_title,
            "author_id": r.author_id,
            "common_likers": r.common_likers,
        }
        for r in rows
    ]