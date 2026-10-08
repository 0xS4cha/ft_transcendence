from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class UnitStat(Base):
    __tablename__ = "unit_stat"

    unit: Mapped[str] = mapped_column("unit", primary_key=True)
    count: Mapped[int] = mapped_column()
    place: Mapped[int] = mapped_column()
    wins: Mapped[int] = mapped_column()
    top4: Mapped[int] = mapped_column()
    items: Mapped[dict[str, int]] = mapped_column("items", JSON)
