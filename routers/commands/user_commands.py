from datetime import datetime
from re import Match

from aiogram import Router, types, F
from magic_filter import RegexpMode

from config import settings
from models import Location, Sale
from routers.kb import (
    milk_keyboard,
    cities_keyboard,
    sales_keyboard,
    supplies_report_keyboard,
    sales_report_by_name_keyboard,
    general_report_keyboard,
)
from services.milk import (
    create_milk_supply_service,
    create_milk_sold_service,
    get_supplies_between_dates_service,
    get_supplies_by_buyer_name_between_dates_service,
    supplies_general_report_service,
)
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
        text='Enter only quantity, if you enter today.\n'
             'Otherwise - quantity and date.\n'
             'Example:\n'
             '    4.45\n'
             '    25.05.2025',
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == 'sold',
)
async def milk_sold_handler(message: types.Message):

    await message.answer(
        text='Enter name, quantity and price, if you enter today.\n'
             'Otherwise - name, quantity, price and date.\n'
             'Example:\n'
             '    Murari Mohini\n'
             '    2.3\n'
             '    100\n'
             '    25.05.2025\n'
             'Or select a frequently used preset ⬇️',
        reply_markup=sales_keyboard(),
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == 'supplies report',
)
async def supplies_report_handler(message: types.Message):
    await message.answer(
        text='Enter price per liter like this:\n'
             '<i>"Liter=35"</i>\n'
             'Or select a frequently used preset ⬇️',
        reply_markup=supplies_report_keyboard(),
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == 'sales report by name',
)
async def sales_report_by_name_handler(message: types.Message):
    await message.answer(
        text='Enter buyer <b>name</b> or his part,\n'
             '<b>start day</b>, <b>end day</b> like this:\n'
             '<i>"Murari\n'
             '01.04.2025\n'
             '30.04.2025"</i>\n'
             'Or select a frequently used preset ⬇️',
        reply_markup=sales_report_by_name_keyboard(),
    )


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.lower() == 'general report',
)
async def general_report_handler(message: types.Message):
    await message.answer(
        text='Enter <b>start day</b>, <b>end day</b> like this:\n'
             '<i>"01.04.2025\n'
             '30.04.2025"</i>\n'
             'Or select a frequently used preset ⬇️',
        reply_markup=general_report_keyboard(),
    )


@router.message(
    F.text.regexp(
        r'^(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('dates')
)
async def supplies_general_report_handler(message: types.Message, dates: Match[str]):
    text: str = await supplies_general_report_service(
        start_date=dates.group(1),
        end_date=dates.group(2),
    )
    await message.answer(text=text)


@router.message(
    F.text.regexp(
        r'^([a-zA-Z ]+)\n'
        r'(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('match')
)
async def supplies_report_by_buyer_name_between_dates(message: types.Message, match: Match[str]):
    text: str = await get_supplies_by_buyer_name_between_dates_service(
        name_part=match.group(1),
        start_date=match.group(2),
        end_date=match.group(3),
    )
    await message.answer(text=text)


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(
        r'^[Ll]iter=(\d+)\n'
        r'(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('match')
)
async def supplies_report_between_dates(message: types.Message, match: Match[str]):
    text: str = await get_supplies_between_dates_service(
        price=int(match.group(1)),
        start_date=match.group(2),
        end_date=match.group(3),
    )
    await message.answer(text=text)


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(
        r'^([A-Za-z ]+)\n'
        r'(\d+(\.\d{1,2})?)\n'
        r'(\d+)'
        r'(\n\d{2}\.\d{2}\.\d{4})?$',
        mode=RegexpMode.MATCH,
    ).as_('match'),
)
async def milk_sold_getter_handler(message: types.Message, match: Match[str]):
    try:
        saved_sale: Sale = await create_milk_sold_service(match=match)
        await message.answer(
            text='Your input has been saved as\n'
                 f'{saved_sale.name.name}\n'
                 f'{saved_sale.quantity} liters\n'
                 f'{saved_sale.price}',
        )
    except ValueError as e:
        await message.answer(f'❌ {e}')


@router.message(
    F.from_user.id.in_(settings.admin_ids),
    F.text.regexp(
        r'^\d+(\.\d{1,2})?'
        r'(\n\d{2}\.\d{2}\.\d{4})?$',
        mode=RegexpMode.MATCH,
    ).as_('supply'),
)
async def milk_took_getter_handler(message: types.Message, supply: Match[str]):
    supply: str = supply.group()
    try:
        saved_supply = await create_milk_supply_service(supply=supply)
        await message.answer(
            text='Your input has been saved as\n'
                 f'{saved_supply.quantity} liters\n'
                 f'{datetime.strptime(str(saved_supply.current_date), '%Y-%m-%d').strftime('%d.%m.%Y')}',
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
    F.text.regexp(r'^(.+?)\n(-?\d+\.\d+)\n(-?\d+\.\d+)$', mode=RegexpMode.MATCH).as_('location_string'),
)
async def create_location_handler(message: types.Message, location_string: Match[str]):
    location_string: str = location_string.group()
    await create_location_service(
        location_string=location_string,
        message=message,
    )
    locations: list[Location] = await get_locations_list(user_tg_id=message.from_user.id)
    await message.reply(
        'Done',
        reply_markup=cities_keyboard(locations=locations),
    )
