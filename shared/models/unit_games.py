from .champions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

class ProcessedGame(Base):
    __tablename__ = "processed_game"

    match_id: Mapped[str] = mapped_column("match_id", primary_key=True)

class UnitStat(Base):
    __tablename__ = "unit_stat"

    unit: Mapped[str] = mapped_column("unit", primary_key=True)
    count: Mapped[int] = mapped_column()
    place: Mapped[int] = mapped_column()
    wins: Mapped[int] = mapped_column()
    top4: Mapped[int] = mapped_column()
    items: Mapped[dict[str, int]] = mapped_column("items", JSON)