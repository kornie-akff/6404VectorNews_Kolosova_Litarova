from db.models import Role
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

def create_role(session: Session, role_name: str) -> Role:
    """ Создание новой роли """
    try:
        new_role = Role(role_name=role_name)
        session.add(new_role)
        session.commit()
        session.refresh(new_role)
        return new_role
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Ошибка: Роль с именем '{role_name}' уже существует!")

def get_role_by_id(session: Session, role_id: int) -> Role:
    """ Получение роли по id """
    role = session.get(Role, role_id)
    if not role:
        raise LookupError(f"Ошибка: Роли с ID {role_id} не существует!")    
    return role

def get_all_roles(session: Session) -> list[Role]:
    """ Получение списка всех ролей """
    all_roles = select(Role)
    return list(session.scalars(all_roles).all())

def update_role(session: Session, role_id: int, new_role_name: str) -> Role:
    """ Изменение данных о роли (название) """
    role = get_role_by_id(session, role_id)
    try:
        role.role_name = new_role_name
        session.commit()
        session.refresh(role)
        return role
    except IntegrityError:
        session.rollback()  # откатываем транзакцию
        raise ValueError(f"Ошибка: Роль с именем '{new_role_name}' уже существует!")

def delete_role(session: Session, role_id: int) -> str:
    """ Удаление роли, но только в случае, если пользователей с такой ролью не существует """
    role = get_role_by_id(session, role_id)
    try:
        session.delete(role)
        session.commit()  # проверка: есть ли уже пользователи с такой ролью
        return f"Роль '{role.role_name}' успешно удалена"
    except IntegrityError:
        session.rollback()
        raise RuntimeError(f"Ошибка: Не удалось удалить роль '{role.role_name}', так как существуют users с данной ролью!")
