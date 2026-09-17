from shared.database import Base
from sqlalchemy.orm import Mapped, mapped_column, UniqueConstraint, CheckConstraint
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import Enum as SAEnum
from enum import Enum

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


# CREATE FUNCTION sort_uids()
# RETURNS TRIGGER
# LANGUAGE plpgsql
# AS
# $$
# DECLARE
#     temp1 INTEGER;
#     temp2 INTEGER;
# BEGIN
#     temp1 := NEW.uid1;
#     temp2 := NEW.uid2;

#     NEW.uid1 := LEAST(temp1, temp2);
#     NEW.uid2 := GREATEST(temp1, temp2);

#     RETURN NEW;
# END;
# $$;


# CREATE TRIGGER sort_trigger
# BEFORE INSERT ON friends
# FOR EACH ROW EXECUTE FUNCTION sort_uids();