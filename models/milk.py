from datetime import date

from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base


class BuyerName(Base):
    name: Mapped[str] = mapped_column(unique=True)
    sales: Mapped[list['Sale']] = relationship(back_populates='name')


class Supply(Base):
    __tablename__ = 'supplies'

    current_date: Mapped[date] = mapped_column(
        unique=True,
        default=date.today(),
        server_default=func.current_date(),
    )
    quantity: Mapped[float] = mapped_column(default=0, server_default='0')

    sales: Mapped[list['Sale']] = relationship(secondary='supply_sale', back_populates='supplies')


class Sale(Base):
    buyer_name_id: Mapped[int] = mapped_column(ForeignKey('buyer_names.id'))
    price: Mapped[int] = mapped_column(default=0, server_default='0')
    quantity: Mapped[float]

    name: Mapped['BuyerName'] = relationship(back_populates='sales')
    supplies: Mapped[list['Supply']] = relationship(secondary='supply_sale', back_populates='sales')


class SupplySale(Base):
    __tablename__ = 'supply_sale'
    __table_args__ = (UniqueConstraint('supply_id', 'sale_id'),)

    supply_id: Mapped[int] = mapped_column(ForeignKey('supplies.id'))
    sale_id: Mapped[int] = mapped_column(ForeignKey('sales.id'))
