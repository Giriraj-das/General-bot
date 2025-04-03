from datetime import datetime, date

from db_connections.milk import get_supply, create_supply, update_supply, create_sale
from models import db_helper, Supply


async def create_milk_supply_service(
        supply: str,
):
    parts: list[str] = supply.split()

    create_data: dict[str, float | date] = {
        'quantity': float(parts[0]),
        'current_date': date.today(),
    }
    update_data: dict[str, float] = {
        'quantity': float(parts[0]),
    }

    if len(parts) == 2:
        try:
            entered_date: date = datetime.strptime(parts[1], '%d.%m.%Y').date()
            create_data['current_date'] = entered_date
        except ValueError:
            raise ValueError('Incorrect date')

    async for session in db_helper.session_dependency():
        supply: Supply | None = await get_supply(
            session=session,
            current_date=create_data['current_date']
        )
        if not supply:
            return await create_supply(
                session=session,
                supply_data=create_data,
            )
        else:
            return await update_supply(
                session=session,
                supply=supply,
                supply_data=update_data,
            )


async def create_milk_sold_service(
        sale: str,
):
    parts: list[str] = sale.split('\n')

    sale_data: dict[str, str | float | int | date] = {
        'name': parts[0],
        'quantity': float(parts[1]),
        'price': int(parts[2]),
        'current_date': date.today(),
    }
    if len(parts) == 4:
        try:
            entered_date: date = datetime.strptime(parts[3], '%d.%m.%Y').date()
            sale_data['current_date'] = entered_date
        except ValueError:
            raise ValueError('Incorrect date')

    async for session in db_helper.session_dependency():
        return await create_sale(
            session=session,
            sale_data=sale_data,
        )
