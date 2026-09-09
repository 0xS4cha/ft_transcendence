from sqlalchemy.orm import Mapped, mapped_column

from shared.models.champions import Base


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