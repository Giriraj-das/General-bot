from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from routers.kb import add_city
from utils import get_weather

router = Router(name=__name__)


@router.callback_query(F.data == add_city)
async def weather_by_city(callback: CallbackQuery):
    print(add_city)


@router.callback_query()
async def weather_by_location(callback: CallbackQuery):
    city, latitude, longitude = callback.data.split(sep='-')
    weather = await get_weather(latitude=latitude, longitude=longitude)
    print(weather)
    await callback.message.answer(
        text=f'The weather of {city}\n'
             f'elevation: <b>{weather['elevation']}m</b>\n'
             f'rain: <b>{weather['current']['rain']}{weather['current_units']['rain']}</b>\n'
             f'temperature: <b>{weather['current']['temperature_2m']}{weather['current_units']['temperature_2m']}</b>\n'
             f'precipitation: <b>{weather['current']['precipitation']}{weather['current_units']['precipitation']}</b>\n'
             f'humidity: <b>{weather['current']['relative_humidity_2m']}{weather['current_units']['relative_humidity_2m']}</b>\n'
             f'wind direction: <b>{weather['current']['wind_direction_10m']}{weather['current_units']['wind_direction_10m']}</b>\n'
             f'wind speed: <b>{weather['current']['wind_speed_10m']}{weather['current_units']['wind_speed_10m']}</b>\n',
        parse_mode=ParseMode.HTML,
    )
