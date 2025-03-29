from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from models import Base

if TYPE_CHECKING:
    from models import Location


class User(Base):
    user_tg_id: Mapped[int]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]

    # many-to-many relationship to Location, bypassing the `UserLocation` class
    locations: Mapped[list['Location']] = relationship(
        secondary='user_location',
        back_populates='users',
    )
