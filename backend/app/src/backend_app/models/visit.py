from sqlalchemy.orm import Mapped, mapped_column

from shared.models.champions import Base


class   VisitModel(Base):
    __tablename__ = "visit_model"

    id: Mapped[str] = mapped_column("id", primary_key=True)
    date: Mapped[str] = mapped_column(index=True)
