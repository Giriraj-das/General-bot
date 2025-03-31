from re import Match

from aiogram import Router, types, F
from magic_filter import RegexpMode

from models import Location
from routers.kb import milk_keyboard, cities_keyboard
from services.weather import create_location_service, get_locations_list

router = Router(name=__name__)


@router.message(F.text.lower() == 'milk')
async def milk_handler(message: types.Message):
    await message.answer(
        text='Select item',
        reply_markup=milk_keyboard(),
    )


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
