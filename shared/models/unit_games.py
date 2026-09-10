from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .champions import Base


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

class PerDayStats(Base):
    __tablename__ = "per_day_stats"

    date: Mapped[str] = mapped_column("date", primary_key=True)
    goldWasted: Mapped[int] = mapped_column()
    totalGames: Mapped[int] = mapped_column()
    totalGameLength: Mapped[float] = mapped_column()