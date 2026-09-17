import datetime

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    date: Mapped[datetime.date] = mapped_column(Date)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    owner: Mapped[UserModel] = relationship( # noqa: F821
        "UserModel",
        back_populates="messages",
    )
    content: Mapped[str] = mapped_column()
