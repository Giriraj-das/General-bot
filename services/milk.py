from datetime import datetime, date
from decimal import Decimal

from db_connections.milk import (
    get_supply,
    create_supply,
    update_supply,
    create_sale,
    get_supplies_between_dates,
    get_supplies_by_name_between_dates,
)
from models import db_helper, Supply, Sale


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


async def get_supplies_between_dates_service(
        price: int,
        start_date: str,
        end_date: str,
) -> str:
    start_date_db: date = datetime.strptime(start_date, "%d.%m.%Y").date()
    end_date_db: date = datetime.strptime(end_date, "%d.%m.%Y").date()

    supplies: list[Supply] = []
    async for session in db_helper.session_dependency():
        supplies = await get_supplies_between_dates(
            session=session,
            start_date=start_date_db,
            end_date=end_date_db,
        )

    price = Decimal(str(price))
    text: str = (f'<b>From {start_date} to {end_date}</b>\n'
                 f'<i>1 liter = {price}₹</i>\n\n')
    total_quantity: Decimal = Decimal('0.00')

    for supply in supplies:
        quantity: Decimal = Decimal(str(supply.quantity))
        text += f'{supply.current_date.day} - {quantity}\n'
        total_quantity += quantity

    text += f'\n<b>{total_quantity} liters</b>\n'
    text += f'<b>{total_quantity * price} ₹</b>'
    return text


async def get_supplies_by_buyer_name_between_dates_service(
        name_part: str,
        start_date: str,
        end_date: str,
) -> str:
    start_date_db: date = datetime.strptime(start_date, "%d.%m.%Y").date()
    end_date_db: date = datetime.strptime(end_date, "%d.%m.%Y").date()

    supplies: list[Supply] = []
    async for session in db_helper.session_dependency():
        supplies = await get_supplies_by_name_between_dates(
            session=session,
            name_part=name_part,
            start_date=start_date_db,
            end_date=end_date_db,
        )

    text: str = f'<b>From {start_date} to {end_date}</b>\n\n'
    total_quantity: Decimal = Decimal('0.00')
    total_price: Decimal = Decimal('0.00')

    for supply in supplies:
        sales: str = ''
        for sale in supply.sales:
            price: Decimal = Decimal(str(sale.price))
            quantity: Decimal = Decimal(str(sale.quantity))

            sales += f'            {sale.name.name} {price}₹ {quantity}l\n'
            total_quantity += quantity
            total_price += price * quantity

        text += f'🔹 {supply.current_date}\n{sales}'

    text += f'\n<b>{total_quantity} liters</b>\n'
    text += f'<b>{total_price} ₹</b>'
    return text
