from db.models import Tag
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


def create_tag(session: Session, tag_name: str) -> Tag:
    """ Создание нового тега """
    try:
        new_tag = Tag(tag_name=tag_name)
        session.add(new_tag)
        session.commit()
        session.refresh(new_tag)
        return new_tag
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Ошибка: Тег с именем {tag_name} уже существует!")

def get_tag_by_id(session: Session, tag_id: int) -> Tag:
    """ Получение тега по id """
    tag = session.get(Tag, tag_id)
    if not tag:
        raise LookupError(f"Ошибка: Тега с ID {tag_id} не существует!")    
    return tag

def get_all_tags(session: Session) -> list[Tag]:
    """ Получение списка всех тегов """
    all_tags = select(Tag)
    return list(session.scalars(all_tags).all())

def update_tag(session: Session, tag_id: int, new_tag_name: str) -> Tag:
    """ Изменение данных о теге (название) """
    tag = get_tag_by_id(session, tag_id)
    try:
        tag.tag_name = new_tag_name
        session.commit()
        session.refresh(tag)
        return tag
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Ошибка: Тег с именем {new_tag_name} уже существует!")

def delete_tag(session: Session, tag_id: int) -> str:
    """ Удаление тега """
    tag = get_tag_by_id(session, tag_id)
    session.delete(tag)
    session.commit() 
    return f"Тег '{tag.tag_name}' успешно удалён"
