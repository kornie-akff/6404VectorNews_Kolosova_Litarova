from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, DateTime, func
from datetime import datetime

class Article(Base):
    """ Статья, опубликованная пользователем с ролью admin """
    __tablename__ = "articles"

    article_id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    article_title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # связь с автором статьи (N:1)
    author: Mapped["User"] = relationship(foreign_keys=[author_id], back_populates="articles")  # type: ignore
    # связь с тегами статьи через article_tags (M:N)
    tags: Mapped[list["Tag"]] = relationship(secondary="article_tags", back_populates="articles")  # type: ignore
    # связь с пользователями, лайкнувшими стаью через likes (M:N)
    liked_by: Mapped[list["User"]] = relationship(secondary="likes", back_populates="user_likes")  # type: ignore

    def __repr__(self):
        return f'Article(article_id={self.article_id}, author_id={self.author_id}, article_titl ={self.article_title}, created_time={self.created_time})'