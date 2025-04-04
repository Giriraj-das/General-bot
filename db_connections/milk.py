from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from models import Supply, Sale, BuyerName


async def get_supply(
        session: AsyncSession,
        current_date: date,
) -> Supply | None:
    return await session.scalar(
        select(Supply)
        .where(Supply.current_date == current_date)
    )


async def create_supply(
        session: AsyncSession,
        supply_data: dict[str, date | float],
) -> Supply:
    supply = Supply(**supply_data)
    session.add(supply)
    await session.commit()

    return await session.scalar(
        select(Supply)
        .where(Supply.id == supply.id)
    )


async def update_supply(
        session: AsyncSession,
        supply: Supply,
        supply_data: dict[str, float],
):
    for name, value in supply_data.items():
        setattr(supply, name, value)
    await session.commit()

    return await session.scalar(
        select(Supply)
        .where(Supply.id == supply.id)
    )


async def create_sale(
        session: AsyncSession,
        sale_data: dict[str, str | float | int | date],
) -> Sale:
    buyer: BuyerName | None = await session.scalar(
        select(BuyerName)
        .where(BuyerName.name == sale_data['name'])
    )
    if not buyer:
        buyer = BuyerName(name=sale_data['name'])
        session.add(buyer)
        await session.flush()

    sale = Sale(
        buyer_name_id=buyer.id,
        quantity=sale_data['quantity'],
        price=sale_data['price'],
    )
    session.add(sale)
    await session.flush()

    supply: Supply | None = await session.scalar(
        select(Supply)
        .options(joinedload(Supply.sales))
        .where(Supply.current_date == sale_data['current_date'])
    )
    if not supply:
        supply = Supply(current_date=sale_data['current_date'])
        session.add(supply)

    supply.sales.append(sale)
    await session.commit()

    return await session.scalar(
        select(Sale)
        .options(selectinload(Sale.name))
        .where(Sale.id == sale.id)
    )
