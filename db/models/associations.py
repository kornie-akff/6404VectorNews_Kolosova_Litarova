from db.models.base import Base
from sqlalchemy import ForeignKey, DateTime, func, Table, Column

# связующие между отношениями многие-ко-многим

""" Ассоциативная таблица связи M:N между статьями и тегами с составным PK (article_id, tag_id) """
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", ForeignKey("articles.article_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
)

""" Ассоциативная таблица связи M:N между пользователями и статьями (лайки) c составным PK (user_id, article_id) """
likes = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True),
    Column("article_id", ForeignKey("articles.article_id", ondelete="CASCADE"), primary_key=True),
    Column("like_time", DateTime(timezone=True), server_default=func.now())
)
