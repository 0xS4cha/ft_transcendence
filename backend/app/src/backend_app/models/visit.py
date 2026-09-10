import datetime

from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class   VisitModel(Base):
    __tablename__ = "visit_model"

    date: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)
