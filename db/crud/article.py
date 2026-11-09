from db.models import Article
from db.crud.user import get_user_by_id
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

def create_article(session: Session, article_title: str, content: str, author_id: int) -> Article:
    """ Создание новой статьи админом """
    author = get_user_by_id(session, author_id)
    if author.role.role_name != "admin":
        raise PermissionError(f"Ошибка: Пользователь с ID {author_id} не является администратором и не может публиковать статьи!")
    try:
        new_article = Article(article_title=article_title, content=content, author_id=author_id)
        session.add(new_article)
        session.commit()
        session.refresh(new_article) # получаем article_id
        return new_article
    except IntegrityError:
        session.rollback()
        raise LookupError(f"Ошибка: Автора с ID {author_id} не существует!")

def get_article_by_id(session: Session, article_id: int) -> Article:
    """ Получение статьи по id """
    article = session.get(Article, article_id)
    if not article:
        raise ValueError(f"Ошибка: Статьи с ID {article_id} не существует!")    
    return article

def get_all_articles(session: Session) -> list[Article]:
    """ Получение списка всех статей (сначала свежие) """
    articles = select(Article).order_by(Article.created_time.desc())
    return list(session.scalars(articles).all())

def update_article(session: Session, article_id: int, new_article_title: str = None, new_content: str = None) -> Article:
    """ Изменение данных о статье (заголовок, содержание) """
    article = get_article_by_id(session, article_id)
    if new_article_title:
        article.article_title = new_article_title
    if new_content:
        article.content = new_content
    session.commit()
    session.refresh(article)
    return article

def delete_article(session: Session, article_id: int) -> str:
    """ Удаление статьи """
    article = get_article_by_id(session, article_id)
    session.delete(article)
    session.commit() 
    return f"Статья '{article.article_title}' успешно удалена"
