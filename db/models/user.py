from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean

class User(Base):
    """ Пользователь новосного портала"""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False) # внешний ключ
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # связь с ролью пользователя (N:1)
    role: Mapped["Role"] = relationship(back_populates="users") # type: ignore
    # связь автора со статьями (1:N)
    articles: Mapped[list["Article"]] = relationship(foreign_keys="Article.author_id", back_populates="author")  # type: ignore
    # связь со статьями, понравившимися читателю через likes (M:N)
    user_likes: Mapped[list["Article"]] = relationship(secondary="likes", back_populates="liked_by")  # type: ignore
    # связь с тегами, на которые подписан читатель через промежуточный класс (M:N -> 1:N)
    user_subscriptions: Mapped[list["TagSubscription"]] = relationship(back_populates="user", cascade="all, delete-orphan")  # type: ignore

    def __repr__(self):
        return f'User(user_id={self.user_id}, username={self.username}, email={self.email}, role_id={self.role_id}, is_active={self.is_active})'
 
