from db.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Tag(Base):
    """ Тег, которым маркируются статьи """
    __tablename__ = "tags"

    tag_id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # связь со статьями, маркированными тегом через article_tags (M:N)
    articles: Mapped[list["Article"]] = relationship(secondary="article_tags", back_populates="tags") # type: ignore
    # связь с читателями, подписанными на тег через промежуточный класс (M:N -> 1:N)
    tag_subscriptions: Mapped[list["TagSubscription"]] = relationship(back_populates="tag", cascade="all, delete-orphan") # type: ignore

    def __repr__(self):
        return f'Tag(tag_id={self.tag_id}, tag_name={self.tag_name})'