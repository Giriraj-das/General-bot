from aiogram import Router, types, F

from db_connections.weather import get_locations_by_user_tg_id
from models import db_helper, Location
from routers.kb import milk_keyboard, cities_keyboard

router = Router(name=__name__)


@router.message(F.text.lower() == 'milk')
async def handle_help(message: types.Message):
    await message.answer(
        text='Select item',
        reply_markup=milk_keyboard(),
    )


@router.message(F.text.lower() == 'weather')
async def show_cities_list(message: types.Message):
    cities: list[Location] = []
    async for session in db_helper.session_dependency():
        cities = await get_locations_by_user_tg_id(
            session=session,
            user_tg_id=message.from_user.id,
        )

    await message.answer(
        text='Select a city or add it.',
        reply_markup=cities_keyboard(cities),
    )
