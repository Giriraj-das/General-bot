from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, with_loader_criteria

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
) -> Supply:
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
    if buyer is None:
        buyer = BuyerName(name=sale_data['name'])
        session.add(buyer)
        await session.flush()

    sale: Sale | None = await session.scalar(
        select(Sale)
        .where(
            Sale.buyer_name_id == buyer.id,
            Sale.quantity == sale_data['quantity'],
            Sale.price == sale_data['price'],
        )
    )
    if sale is None:
        sale = Sale(
            buyer_name_id=buyer.id,
            quantity=sale_data['quantity'],
            price=sale_data['price'],
        )
        session.add(sale)
        await session.flush()

    supply: Supply | None = await session.scalar(
        select(Supply)
        .where(Supply.current_date == sale_data['current_date'])
        .options(joinedload(Supply.sales))
    )
    if supply is None:
        supply = Supply(current_date=sale_data['current_date'])
        session.add(supply)

    supply.sales.append(sale)
    await session.commit()

    return await session.scalar(
        select(Sale)
        .options(selectinload(Sale.name))
        .where(Sale.id == sale.id)
    )


async def get_supplies_between_dates(
        session: AsyncSession,
        start_date: date,
        end_date: date,
) -> list[Supply]:
    supplies = await session.scalars(
        select(Supply)
        .filter(Supply.current_date.between(start_date, end_date))
        .order_by(Supply.current_date)
    )
    return list(supplies)


async def get_supplies_by_name_between_dates(
        session: AsyncSession,
        name_part: str,
        start_date: date,
        end_date: date,
) -> list[Supply]:
    name_filter = BuyerName.name.ilike(f"%{name_part}%")
    result = await session.execute(
        select(Supply)
        .join(Supply.sales)
        .join(Sale.name)
        .where(
            Supply.current_date.between(start_date, end_date),
            name_filter,
        )
        .order_by(Supply.current_date)
        .options(
            joinedload(Supply.sales).joinedload(Sale.name),
            with_loader_criteria(
                Sale,
                lambda cls: cls.name.has(name_filter),
                include_aliases=True,
            )
        )
    )
    return list(result.unique().scalars())


async def get_supplies_with_all_sales(
        session: AsyncSession,
        start_date: date,
        end_date: date,
) -> list[Supply]:
    supplies = await session.execute(
        select(Supply)
        .outerjoin(Supply.sales)
        .outerjoin(Sale.name)
        .where(
            Supply.current_date.between(start_date, end_date),
        )
        .order_by(Supply.current_date)
        .options(
            joinedload(Supply.sales).joinedload(Sale.name),
        )
    )
    return list(supplies.unique().scalars())
