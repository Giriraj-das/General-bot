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

    locations: Mapped[list['Location']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
