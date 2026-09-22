from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class   Unit(Base):
    __tablename__ = "units"

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
    icon: Mapped[str] = mapped_column(
        String,
        nullable=False
    )