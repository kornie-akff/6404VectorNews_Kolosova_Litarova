from db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

class Role(Base):
    """ Роль пользователя """
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # связь с пользователями, которым пренадлежит эта роль (1:N)
    users: Mapped[list["User"]] = relationship(back_populates="role") # type: ignore

    def __repr__(self):
        return f'Role(role_id={self.role_id}, role_name={self.role_name})'