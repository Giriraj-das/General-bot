from datetime import datetime, date

from db_connections.milk import create_supply
from models import db_helper


async def create_milk_supply_service(
        supply: str,
):
    parts = supply.split()

    supply_data = {}
    if len(parts) == 1:
        supply_data = {'quantity': float(parts[0])}
    elif len(parts) == 2:
        try:
            entered_date: date = datetime.strptime(parts[0], '%d.%m.%Y').date()
            supply_data = {
                'current_date': entered_date,
                'quantity': float(parts[1]),
            }
        except ValueError:
            raise ValueError('Incorrect date')

    async for session in db_helper.session_dependency():
        return await create_supply(
            session=session,
            supply_data=supply_data,
        )
