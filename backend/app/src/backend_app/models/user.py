from    backend_app.database    import  Base
from    sqlalchemy.orm          import  Mapped, mapped_column
from    sqlalchemy              import  Integer

class   UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column()