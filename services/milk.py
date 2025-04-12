from datetime import datetime, date

from db_connections.milk import (
    get_supply,
    create_supply,
    update_supply,
    create_sale,
    get_supplies_by_current_month,
)
from models import db_helper, Supply, Sale


async def get_supplies_service(price: int) -> str:
    today = date.today()
    first_day_of_current_month = date(today.year, today.month, 1)

    supplies: list[Supply] = []
    async for session in db_helper.session_dependency():
        supplies = await get_supplies_by_current_month(
            session=session,
            first_day=first_day_of_current_month,
        )

    text: str = (f'<b>{today.strftime('%B')}</b>\n'
                 f'1 liter = {price}₹\n\n')
    total_quantity: int = 0
    for supply in supplies:
        text += f'{supply.current_date.day} - {supply.quantity}\n'
        total_quantity += supply.quantity
    text += f'\n<b>{total_quantity} liters</b>\n'
    text += f'<b>{total_quantity * price} ₹</b>'

    return text


async def create_milk_supply_service(
        supply: str,
) -> Supply:
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
) -> Sale:
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
