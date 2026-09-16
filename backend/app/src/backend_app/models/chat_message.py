import datetime

from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base
from backend_app.models.user import UserModel


class   ChatMessage(Base):
    __tablename__ = "chat_message"

    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    owner: Mapped[UserModel] = relationship(
        back_populates="users", cascade="all, delete-orphan", uselist=False
    )
    content: Mapped[str] = mapped_column()
