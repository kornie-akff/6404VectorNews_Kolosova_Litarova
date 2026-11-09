from db.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean

class TagSubscription(Base):
    """ Подписка пользователя на тег с настройкой уведомлений.
    Ассоциативная сущность для связи M:N между пользователями и тегами """
    __tablename__ = "tag_subscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
    is_notification_on: Mapped[bool] = mapped_column(Boolean, default=False) # важно! изменяемое поле

    user: Mapped["User"] = relationship(back_populates="user_subscriptions")  # type: ignore
    tag: Mapped["Tag"] = relationship(back_populates="tag_subscriptions") # type: ignore

    def __repr__(self):
        return f'TagSubscription(user_id={self.user_id}, tag_id={self.tag_id}, is_notification_on={self.is_notification_on})'
