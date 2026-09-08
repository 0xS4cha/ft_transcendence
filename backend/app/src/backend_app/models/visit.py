from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date
from backend_app.database import Base
from datetime import date


class   VisitModel(Base):
    __tablename__ = "visit_model"

    date: Mapped[date] = mapped_column(Date, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)
