from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models import Base

if TYPE_CHECKING:
    from models import User


class Location(Base):
    city: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    # many-to-many relationship to User, bypassing the `UserLocation` class
    users: Mapped[list['User']] = relationship(
        secondary='user_location',
        back_populates='locations',
    )
