from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class   Augment(Base):
    __tablename__ = "augments"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    rarity: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    rounds: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False
    )
    icon: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    
