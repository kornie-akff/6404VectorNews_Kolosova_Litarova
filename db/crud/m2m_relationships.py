from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from db.models import User, Article, Tag, TagSubscription
from db.crud.user import get_user_by_id
from db.crud.article import get_article_by_id
from db.crud.tag import get_tag_by_id

# функционал работы со связями многие-ко-многим

def add_tag_to_article(session: Session, article_id: int, tag_id: int) -> Article:
    """ Администратор выбирает ОДИН тег для статьи при публикации """
    article = get_article_by_id(session, article_id)
    tag = get_tag_by_id(session, tag_id)   
    if tag not in article.tags:
        article.tags.append(tag)
        session.commit()
        session.refresh(article)
    return article

def remove_tag_from_article(session: Session, article_id: int, tag_id: int) -> Article:
    """ Администратор удаляет ОДИН тег для статьи при публикации """
    article = get_article_by_id(session, article_id)
    tag = get_tag_by_id(session, tag_id)  
    if tag in article.tags:
        article.tags.remove(tag)
        session.commit()
        session.refresh(article)
    return article

def get_article_tags(session: Session, article_id: int) -> list[Tag]:
    """ Получение списка тегов статьи """
    article = get_article_by_id(session, article_id) 
    return list(article.tags)

def get_articles_by_tag(session: Session, tag_id: int) -> list[Article]:
    """ Поиск статей по тегу начиная от самых новых """
    tag = get_tag_by_id(session, tag_id)   
    return sorted(tag.articles, key=lambda x: x.created_time, reverse=True)

def like_article(session: Session, user_id: int, article_id: int) -> Article:
    """ Читатель ставит лайк статье """
    user = get_user_by_id(session, user_id) 
    article = get_article_by_id(session, article_id) 
    if user not in article.liked_by:
        article.liked_by.append(user)
        session.commit()
        session.refresh(article)
    return article

def unlike_article(session: Session, user_id: int, article_id: int) -> Article:
    """ Читатель убирает свой лайк статье """
    user = get_user_by_id(session, user_id) 
    article = get_article_by_id(session, article_id)
    if user in article.liked_by:
        article.liked_by.remove(user)
        session.commit()
        session.refresh(article)
    return article

def get_article_likes(session: Session, article_id: int) -> list[User]:
    """ Получение списка пользователей, лайкнувших статью """
    article = get_article_by_id(session, article_id) 
    return list(article.liked_by)

def get_user_likes(session: Session, user_id: int) -> list[Article]:
    """ Получение списка статей, лайкнутые пользователем """
    user = get_user_by_id(session, user_id) 
    return list(user.user_likes)
  
def subscribe_to_tag(session: Session, user_id: int, tag_id: int) -> TagSubscription:
    """ Читатель подписывается на тег """
    get_user_by_id(session, user_id) 
    get_tag_by_id(session, tag_id)
    subscription = TagSubscription(user_id=user_id, tag_id=tag_id)
    session.add(subscription)
    try:
        session.commit()
        session.refresh(subscription)
        return subscription
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Ошибка: Пользователь с ID {user_id} уже подписан на тег с ID {tag_id}!")

def unsubscribe_from_tag(session: Session, user_id: int, tag_id: int) -> str:
    """ Читатель отписывается от тега """
    get_user_by_id(session, user_id) 
    get_tag_by_id(session, tag_id)
    subscription = session.get(TagSubscription, (user_id, tag_id))
    if not subscription:
        raise LookupError(f"Ошибка: Пользователь с ID {user_id} еще даже не подписан на тег с ID {tag_id}!")  
    session.delete(subscription)
    session.commit()
    return f"Пользователь с ID {user_id} был отписан от тега с ID {tag_id}!"

def get_user_subscriptions(session: Session, user_id: int) -> list[TagSubscription]:
    """ Получение списка подписок на теги читателя """
    user = get_user_by_id(session, user_id) 
    return list(user.user_subscriptions)

def get_tag_subscriptions(session: Session, tag_id: int) -> list[TagSubscription]:
    """ Получение списка подписчиков на тег """
    tag = get_tag_by_id(session, tag_id)
    return list(tag.tag_subscriptions)

def set_notification(session: Session, user_id: int, tag_id: int, enabled: bool) -> TagSubscription:
    """ Настройка уведомлений публикации статей по тегу """
    get_user_by_id(session, user_id)
    get_tag_by_id(session, tag_id)
    subscription = session.get(TagSubscription, (user_id, tag_id))
    if not subscription:
        raise LookupError(f"Ошибка: Пользователь с ID {user_id} не подписан на тег с ID {tag_id}! Для рассылки уведомлений нужно подписаться на тег.")  

    subscription.is_notification_on = enabled
    session.commit()
    session.refresh(subscription)
    return subscription

def get_notification_recipients(session: Session, tag_id: int) -> list[User]:
    """ Получение списка пользователей, подписанных на тег и на рассылку уведомлений, для Notification Service """
    get_tag_by_id(session, tag_id)

    stmt = (
        select(User)
        .join(TagSubscription, TagSubscription.user_id == User.user_id)
        .where(
            TagSubscription.tag_id == tag_id,
            TagSubscription.is_notification_on == True,
            User.is_active == True,
        )
    )
    return list(session.scalars(stmt).all())

def get_notification_recipients_for_article(session: Session, article_id: int) -> dict[int, list[User]]:
    """ Получение словаря, где ключи - теги статьи, значения - списки получателей, для Notification Service при публикации новой статьи """
    article = get_article_by_id(session, article_id)

    result: dict[int, list[User]] = {}
    for tag in article.tags:
        result[tag.tag_id] = get_notification_recipients(session, tag.tag_id)
    return result

def get_user_notification_settings(session: Session, user_id: int) -> list[tuple[Tag, bool]]:
    """ Получение словаря, где ключи - теги, на которые подписан пользователь, значения - включены ли уведомления, 
    для удобного отображения на странице подписок пользователя """
    user = get_user_by_id(session, user_id)
    return [(sub.tag, sub.is_notification_on) for sub in user.user_subscriptions]