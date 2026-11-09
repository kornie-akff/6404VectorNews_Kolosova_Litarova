from db.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

def create_user(session: Session, username: str, email: str, password: str, role_id: int) -> User:
    """ Создание нового пользователя """
    try:
        new_user = User(username=username, email=email, password=password, role_id=role_id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user) # получаем user_id
        return new_user
    except IntegrityError:
        session.rollback()  # откатываем транзакцию
        raise ValueError(f"Ошибка: Пользователь с именем '{username}' или почтой '{email}' уже существует!")

def get_user_by_id(session: Session, user_id: int) -> User:
    """ Получение пользователя по id """
    user = session.get(User, user_id)
    if not user:
        raise LookupError(f"Ошибка: Пользователя с ID {user_id} не существует!")  
    return user  

def get_all_users(session: Session) -> list[User]:
    """ Получение списка всех пользователей """
    all_users = select(User)
    return list(session.scalars(all_users).all())

def update_user(session: Session, user_id: int, new_username: str = None, new_email: str = None, new_password: str = None) -> User:
    """ Изменение данных о пользователе (имя, почта, пароль) """
    user = get_user_by_id(session, user_id)
    try:
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Ошибка: Данные username или email не уникальны!")

def deactive_user(session: Session, user_id: int) -> User:
    """ Дезактивация профиля пользователя, а не прямое удаление """
    user = get_user_by_id(session, user_id)
    user.is_active = False
    session.commit()
    session.refresh(user)
    return user