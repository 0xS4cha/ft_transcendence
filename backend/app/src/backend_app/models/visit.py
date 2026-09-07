from sqlalchemy.orm import Mapped, mapped_column
from backend_app.database import Base


class   VisitModel(Base):
    __tablename__ = "visit"

    id: Mapped[str] = mapped_column("id", primary_key=True)
    date: Mapped[str] = mapped_column(index=True)
    