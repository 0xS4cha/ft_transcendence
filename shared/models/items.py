from sqlalchemy import ARRAY, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class   Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )
    avg_place: Mapped[float] = mapped_column(
        "avgPlace",
        Float,
        nullable=False
    )
    winrate: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    frequency: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    composition: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False
    )
    icon: Mapped[str] = mapped_column(
        String,
        nullable=False
    )