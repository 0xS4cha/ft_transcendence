from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger

from shared.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    date: Mapped[int] = mapped_column(BigInteger)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    owner: Mapped[UserModel] = relationship( # noqa: F821
        "UserModel",
        back_populates="messages",
    )
    content: Mapped[str] = mapped_column()
