from sqlalchemy.orm import Mapped

from models import Base


class Location(Base):
    city: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
