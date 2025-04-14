from datetime import datetime, date
from decimal import Decimal
from re import Match

from db_connections.milk import (
    get_supply,
    create_supply,
    update_supply,
    create_sale,
    get_supplies_between_dates,
    get_supplies_by_name_between_dates,
    get_supplies_with_all_sales,
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
        match: Match[str],
) -> Sale:
    sale_data: dict[str, str | float | int | date] = {
        'name': match.group(1),
        'quantity': float(match.group(2)),
        'price': int(match.group(4)),
        'current_date': date.today(),
    }
    current_date: str | None = match.group(5) if match.lastindex >= 5 else None

    if current_date is not None:
        try:
            entered_date: date = datetime.strptime(current_date, '%d.%m.%Y').date()
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


async def supplies_general_report_service(
        start_date: str,
        end_date: str,
) -> str:
    start_date_db: date = datetime.strptime(start_date, "%d.%m.%Y").date()
    end_date_db: date = datetime.strptime(end_date, "%d.%m.%Y").date()

    supplies: list[Supply] = []
    async for session in db_helper.session_dependency():
        supplies = await get_supplies_with_all_sales(
            session=session,
            start_date=start_date_db,
            end_date=end_date_db,
        )

    text: str = f'<b>From {start_date} to {end_date}</b>\n\n'
    supply_total_quantity: Decimal = Decimal('0.00')
    sale_total_quantity: Decimal = Decimal('0.00')

    for supply in supplies:
        sales: str = ''
        supply_quantity: Decimal = Decimal(str(supply.quantity))

        for sale in supply.sales:
            quantity: Decimal = Decimal(str(sale.quantity))

            sales += f'            {sale.name.name} {quantity}l\n'
            sale_total_quantity += quantity

        text += f'🔹 <b>{supply.current_date} {supply_quantity}l</b>\n{sales}'
        supply_total_quantity += supply_quantity

    text += f'\n<b>Supplies {supply_total_quantity} liters</b>'
    text += f'\n<b>Sales {sale_total_quantity} liters</b>'
    text += f'\n<b>Rest {supply_total_quantity - sale_total_quantity} liters</b>'
    return text
