from db.connect import engine, SessionLocal
from db.models import Base
from db import crud, data_for_demo, models

# Сценарии

def scenario_read_users(session, data) -> None:
    print("---Read users---")

    victoria = data["users"]["Victoria"]

    fetched = crud.get_user_by_id(session, victoria.user_id)
    print (f"get_user_by_id(victoria): {fetched}")

    all_users = crud.get_all_users(session)
    print(f"get_all_users (amount): {len(all_users)}")
    for u in all_users:
        print(f"    - {u} | role={u.role.role_name} | active={u.is_active}")


def scenario_update_user(session, data) -> None:
    print("---Update user info---")

    victoria = data["users"]["Victoria"]
    updated = crud.update_user(
        session,
        victoria.user_id,
        new_email="MURRR@mail.ru",
        new_username="Vika",
    )
    print(f"update_user(Victoria): {updated}")


def scenario_read_tags(session, data) -> None:
    print("---Tags---")

    all_tags = crud.get_all_tags(session)
    print(f"get_all_tags (amount): {len(all_tags)}")
    for t in all_tags:
        print(f"    - {t}")


def scenario_read_articles(session, data) -> None:
    print("---Articles---")

    all_articles = crud.get_all_articles(session)
    print(f"get_all_articles (amount): {len(all_articles)}")
    for a in all_articles:
        print(f"    - {a} | author = {a.author.username}")

def scenario_open_article(session, data) -> None:
    """Читатель кликает на статью — система показывает полный текст."""
    print("---Open article---")

    article_2 = data["articles"]["a2"]
    article = crud.get_article_by_id(session, article_2.article_id)

    print(f"  title:   {article.article_title}")
    print(f"  author:  {article.author.username}")
    print(f"  date:    {article.created_time}")
    print(f"  content: {article.content}")
    print(f"  tags:    {[t.tag_name for t in article.tags]}")

def scenario_article_tags(session, data) -> None:
    print("---Article tags---")

    article_2 = data["articles"]["a2"]
    tags = crud.get_article_tags(session, article_2.article_id)
    print(f"Article_tags {article_2.article_title!r}: {[t.tag_name for t in tags]}")


def scenario_articles_by_tag(session, data) -> None:
    print("---Filter---")

    tag_books = data["tags"]["books"]
    articles = crud.get_articles_by_tag(session, tag_books.tag_id)
    print(f"artices with tag {tag_books.tag_name!r}: {len(articles)}")
    for a in articles:
        print(f"    - {a.article_title} (created_time={a.created_time})")

def scenario_publish_article(session, data) -> None:
    """Админ публикует новую статью."""
    print("---Publish new article---")

    artem = data["users"]["Artem"]
    tag_books = data["tags"]["books"]

    article = crud.create_article(
        session,
        article_title="Наука: новые горизонты",
        content="Обзор последних научных открытий...",
        author_id=artem.user_id,
    )
    crud.add_tag_to_article(session, article.article_id, tag_books.tag_id)
    print(f"  published: {article}")

    # Проверка бизнес-правила
    victoria = data["users"]["Victoria"]
    try:
        crud.create_article(
            session,
            article_title="Попытка читателя",
            content="...",
            author_id=victoria.user_id,
        )
    except PermissionError as e:
        print(f"  reader blocked: {e}")

def scenario_edit_article(session, data) -> None:
    """Админ редактирует статью: теги + заголовок + текст."""
    print("---Edit article---")

    article = data["articles"]["a3"]
    tag_fashion = data["tags"]["fashion"]
    tag_music = data["tags"]["music"]

    found = crud.get_article_by_id(session, article.article_id)
    print(f"  before title: {found.article_title}")
    print(f"  before tags:  {[t.tag_name for t in found.tags]}")

    # удалить тег
    crud.remove_tag_from_article(session, article.article_id, tag_fashion.tag_id)
    # добавить тег
    crud.add_tag_to_article(session, article.article_id, tag_music.tag_id)
    # изменить заголовок и текст
    crud.update_article(
        session,
        article.article_id,
        new_article_title="Мода в СССР: расширенное издание",
        new_content="Обновлённый текст статьи...",
    )

    found = crud.get_article_by_id(session, article.article_id)
    print(f"  after title: {found.article_title}")
    print(f"  after tags:  {[t.tag_name for t in found.tags]}")

def scenario_likes(session, data) -> None:
    print("---Likes---")

    article_1 = data["articles"]["a1"]
    victoria = data["users"]["Victoria"]
    egor = data["users"]["Egor"]

    print(f"a1's likes: {[u.username for u in crud.get_article_likes(session, article_1.article_id)]}")

    print(f"Victoria's likes: {[a.article_title for a in crud.get_user_likes(session, victoria.user_id)]}")

    crud.unlike_article(session, egor.user_id, article_1.article_id)
    print(f"After unlike(Egor, a1): {[u.username for u in crud.get_article_likes(session, article_1.article_id)]}")


def scenario_subscriptions(session, data) -> None:
    print("---Tag subsriptions---")

    victoria = data["users"]["Victoria"]
    tag_books = data["tags"]["books"]

    subs = crud.get_user_subscriptions(session, victoria.user_id)
    print(f"Victoria's subscriptions: {[(s.tag.tag_name, s.is_notification_on) for s in subs]}")

    print(f"Tag's subsriptors {tag_books.tag_name!r}: {[s.user.username for s in crud.get_tag_subscriptions(session, tag_books.tag_id)]}")


def scenario_notifications(session, data) -> None:
    print("---Notifications---")

    tag_books = data["tags"]["books"]
    recipients = crud.get_notification_recipients(session, tag_books.tag_id)
    print(f"Active users with is_notification_on=True по {tag_books.tag_name!r}: {[u.username for u in recipients]}")


def scenario_disactivate(session, data) -> None:
    print("---Disactivate---")

    artem = data["users"]["Artem"]

    artem = crud.deactive_user(session, artem.user_id)
    print(f"Artem after disactivation: {artem} | is_active={artem.is_active}")

    scenario_open_article(session, data)

    egor = data["users"]["Egor"]
    tag_books = data["tags"]["books"]
    
    egor = crud.deactive_user(session, egor.user_id)
    print(f"Egor after disactivation: {egor} | is_active={egor.is_active}")
   
    recipients = crud.get_notification_recipients(session, tag_books.tag_id)
    print(f"Current subsriptors of tag '{tag_books.tag_name}': {[u.username for u in recipients]}")


def scenario_errors(session, data) -> None:
    print("---Errors---")

    # 11.1. Повторный username
    try:
        crud.create_user(
            session,
            username="Vika",      # уже занят после update_user
            email="unique@x.ru",
            password="fghj",
            role_id=data["roles"]["reader"].role_id,
        )
    except ValueError as e:
        print(e)

    # 11.2. Удаление роли с пользователями
    try:
        crud.delete_role(session, data["roles"]["reader"].role_id)
    except ValueError as e:
        print(e)


def scenario_delete_article(session, data) -> None:
    print("---Delete article---")

    article_1 = data["articles"]["a3"]
    print(f"Before (amount): {len(crud.get_all_articles(session))}")

    crud.delete_article(session, article_1.article_id)

    remaining = crud.get_all_articles(session)
    print(f"After (amount): {len(remaining)}")
    for a in remaining:
        print(f"    - {a.article_title}")

    # Проверка каскада: article_tags и likes по удалённой статье
    from sqlalchemy import select
    stmt = select(models.associations.likes).where(models.associations.likes.c.article_id == article_1.article_id)
    print(f"Amount of likes on deleted article: {len(session.execute(stmt).all())}")


def scendrio_liked_articles_tags(session, data):
    print("---All tags of articles user liked---")
    victoria = data["users"]["Victoria"]
    all_liked_articles = crud.get_user_likes(session, victoria.user_id)
    print(f"Victoria's likes: {[a.article_title for a in all_liked_articles]}")
    
    all_tags = {t.tag_name for a in all_liked_articles for t in a.tags}
    print (f"Tags of articles liked by Victoria: {all_tags}")

# Точка входа

def main() -> None:
    # Создаём таблицы 
    Base.metadata.create_all(bind = engine)
    print(f"Tables: { list(Base.metadata.tables.keys())}")

    # Чистим БД от предыдущих запусков, чтобы unique-ограничения не мешали повторному запуску демо.
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    with SessionLocal() as session:
        # Наполняем БД
        data = data_for_demo.seed_all(session)

        # теги статей которые пользователь лайкал
        scendrio_liked_articles_tags(session, data)
        scenario_publish_article(session, data)
        scenario_read_users(session, data) 
        scenario_read_tags(session, data) 
        scenario_read_articles(session, data) 
        scenario_open_article(session, data) 
        scenario_article_tags(session, data)
        scenario_articles_by_tag(session, data)
        scenario_likes(session, data)
        scenario_subscriptions(session, data)
        scenario_notifications(session, data)
        scenario_edit_article(session, data)
        scenario_update_user(session, data)
        scenario_disactivate(session, data) 
        scenario_delete_article(session, data)
        scenario_errors(session, data)



if __name__ == "__main__":
    main()