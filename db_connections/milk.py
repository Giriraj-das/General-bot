from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Supply


async def create_supply(
        session: AsyncSession,
        supply_data: dict[str: date | float],
) -> Supply:
    supply = Supply(**supply_data)
    session.add(supply)
    await session.commit()

    return await session.scalar(
        select(Supply)
        .options(joinedload(Supply.sales))
        .where(Supply.id == supply.id)
    )
