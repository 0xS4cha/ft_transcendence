from enum import Enum

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base


class   Status(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"

class   Friends(Base):
    __tablename__ = "friends"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    requester: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    uid1: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    uid2: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    status: Mapped[Status] = mapped_column(
        SAEnum(
            Status,
            name='friends_status',
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    __table_args__ = (
        UniqueConstraint('uid1', 'uid2', name='uids'),
        CheckConstraint('requester = uid1 OR requester = uid2')
    )





