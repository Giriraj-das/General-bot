from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class UserLocation(Base):
    __tablename__ = 'user_location'
    __table_args__ = (UniqueConstraint('user_id', 'location_id'),)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'))
