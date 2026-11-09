# Добавляем данные в БД для демонстрации работы

from sqlalchemy.orm import Session
from db import crud


def seed_all(session: Session) -> dict:
    """ Наполнение БД тестовыми данными в виде словаря """
    
    # Роли
    admin = crud.create_role(session, "admin")
    reader = crud.create_role(session, "reader")

    # Пользователи 

    user_natasha = crud.create_user( 
        session,
        username = "Natasha",
        email = "dino@gmail.com",
        password = "qwerty",       
        role_id = admin.role_id,
    )

    user_artem = crud.create_user( 
        session,
        username = "Artem",
        email = "privet_artem@mail.ru",
        password = "arbuz",
        role_id = admin.role_id,
    )

    user_victoria = crud.create_user(
        session,
        username = "Victoria",
        email = "murrr@yandex.ru",
        password = "ppp789",
        role_id = reader.role_id,
    )

    user_egor = crud.create_user( 
        session,
        username = "Egor",
        email = "egor@mail.ru",
        password = "123",
        role_id = reader.role_id,
    )

    user_katya = crud.create_user( 
        session,
        username = "Katya",
        email = "katya_photo@mail.ru",
        password = "hanjisung2000",
        role_id = reader.role_id,
    )

    # Теги

    tag_health = crud.create_tag(session, "health")
    tag_books = crud.create_tag(session, "books")
    tag_space = crud.create_tag(session, "space")
    tag_fashion = crud.create_tag(session, "fashion")
    tag_music = crud.create_tag(session, "music")

    # Статьи (автор — админ)

    article_1 = crud.create_article(
        session,
        article_title = "Новым Дозорам быть",
        content = "Сергей Лукьяненко планирует написать продолжение культового цикла о Дозорах",
        author_id = user_artem.user_id,
    )
    article_2 = crud.create_article(
        session,
        article_title = "Что происходит с человеком в космосе",
        content = "Как изменение физических условий влияет на работу человеческого организма",
        author_id = user_artem.user_id,
    )
    article_3 = crud.create_article(
        session,
        article_title = "Мода в СССР",
        content = "Юлия Папушина в своей новой книге Мода в стране дефицита изучила ...",
        author_id = user_natasha.user_id,
    )
    article_4 = crud.create_article(
        session,
        article_title = "Оливер Три разбился на вертолёте – или нет: фанаты заподозрили кумира в обмане",
        content = "Новость о гибели Оливера Три потрясла многочисленных поклонников по всему миру",
        author_id = user_natasha.user_id,
    )

    # Связи M:N: теги статей 

    crud.add_tag_to_article(session, article_1.article_id, tag_books.tag_id)

    crud.add_tag_to_article(session, article_2.article_id, tag_health.tag_id)
    crud.add_tag_to_article(session, article_2.article_id, tag_space.tag_id)

    crud.add_tag_to_article(session, article_3.article_id, tag_books.tag_id)
    crud.add_tag_to_article(session, article_3.article_id, tag_fashion.tag_id)

    crud.add_tag_to_article(session, article_4.article_id, tag_music.tag_id)

    # Лайки

    crud.like_article(session, user_victoria.user_id, article_2.article_id)
    crud.like_article(session, user_egor.user_id, article_1.article_id)
    crud.like_article(session, user_victoria.user_id, article_3.article_id)
    crud.like_article(session, user_katya.user_id, article_3.article_id)

    # Подписки на теги

    crud.subscribe_to_tag(session, user_victoria.user_id, tag_books.tag_id)
    crud.subscribe_to_tag(session, user_egor.user_id, tag_books.tag_id)
    crud.subscribe_to_tag(session, user_victoria.user_id, tag_fashion.tag_id)
    crud.subscribe_to_tag(session, user_egor.user_id, tag_space.tag_id)
    crud.subscribe_to_tag(session, user_katya.user_id, tag_music.tag_id)

    # Настройки уведомлений

    crud.set_notification(session, user_victoria.user_id, tag_books.tag_id, True)
    crud.set_notification(session, user_egor.user_id, tag_space.tag_id, True)
    crud.set_notification(session, user_katya.user_id, tag_music.tag_id, True)

    return {
        "roles": {"admin": admin, "reader": reader},
        "users": {"Natasha": user_natasha, "Artem": user_artem, "Victoria": user_victoria, "Egor": user_egor, "Katya": user_katya},
        "tags": {
            "health": tag_health,
            "books": tag_books,
            "space": tag_space,
            "fashion": tag_fashion,
            "music": tag_music
        },
        "articles": {"a1": article_1, "a2": article_2, "a3": article_3, "a4": article_4},
    }

if __name__ == "__main__":
    from db.connect import Base, engine, SessionLocal
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind = engine)
    with SessionLocal() as session:
        data = seed_all(session)
        print("Data created")
        print("Roles:   ", list(data["roles"].keys()))
        print("Users:  ", list(data["users"].keys()))
        print("Tags:   ", list(data["tags"].keys()))
        print("Articles: ", list(data["articles"].keys()))