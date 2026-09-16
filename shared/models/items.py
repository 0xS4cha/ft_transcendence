from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class   Item(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    avg_place: Mapped[float] = mapped_column("avgPlace", Float)
    winrate: Mapped[float] = mapped_column(Float)
    frequency: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)