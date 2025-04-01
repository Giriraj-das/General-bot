from datetime import datetime
from re import Match

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from magic_filter import RegexpMode

from config import settings
from models import Location
from routers.kb import milk_keyboard, cities_keyboard, sales_keyboard
from services.milk import create_milk_supply_service
from services.weather import create_location_service, get_locations_list

router = Router(name=__name__)


@router.message(F.text.lower() == 'milk')
async def milk_handler(message: types.Message):
    await message.answer(
        text='Select item',
        reply_markup=milk_keyboard(),
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == 'took',
)
async def milk_took_handler(message: types.Message):
    await message.answer(
        text='Enter only number of liters, if you enter today.\n'
             'Otherwise, date and litres.\n'
             'Example:\n'
             '    25.05.2025\n'
             '    4.45',
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(
        r'^(\d{2}\.\d{2}\.\d{4}\n)?\d+(\.\d{1,2})?$',
        mode=RegexpMode.MATCH,
    ).as_('supply'),
)
async def milk_took_getter_handler(message: types.Message, supply: Match[str]):
    supply: str = supply.group()
    try:
        saved_supply = await create_milk_supply_service(supply=supply)
        await message.answer(
            text='Your input was saved as\n'
                 f'{datetime.strptime(str(saved_supply.current_date), '%Y-%m-%d').strftime('%d.%m.%Y')}\n'
                 f'{saved_supply.quantity} liters',
        )
    except ValueError as e:
        await message.answer(f'❌ {e}')


@router.message(F.text.lower() == 'weather')
async def show_cities_list_handler(message: types.Message):
    locations: list[Location] = await get_locations_list(user_tg_id=message.from_user.id)

    await message.answer(
        text='Select a city or add it.',
        reply_markup=cities_keyboard(locations=locations),
    )


@router.message(
    F.text.regexp(r'^(.+?)/(-?\d+\.\d+)/(-?\d+\.\d+)$', mode=RegexpMode.MATCH).as_('location_string'),
)
async def create_location_handler(message: types.Message, location_string: Match[str]):
    location_string: str = location_string.group()
    await create_location_service(
        location_string=location_string,
        message=message
    )
    locations: list[Location] = await get_locations_list(user_tg_id=message.from_user.id)
    await message.reply(
        'Done',
        reply_markup=cities_keyboard(locations=locations),
    )
