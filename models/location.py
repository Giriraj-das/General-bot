from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import User


class Location(Base):
    city: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(
        back_populates='locations',
    )
