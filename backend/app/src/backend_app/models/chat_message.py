import datetime

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base
from backend_app.models.user import UserModel


class   ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    owner_id = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserModel"] = relationship(
        back_populates="messages"
    )
    content: Mapped[str] = mapped_column()
