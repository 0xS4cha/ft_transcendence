from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base
from backend_app.models.chat_message import ChatMessage


class   UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    picture: Mapped[str | None] = mapped_column()
    messages: Mapped[list[ChatMessage]] = relationship( # noqa: F821
        "ChatMessage",
        back_populates="owner",
        cascade="all, delete-orphan",
    )