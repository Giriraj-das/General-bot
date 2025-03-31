from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from models import Location
from routers.kb import add_city, cities_keyboard
from services.weather import get_locations_list
from utils import get_weather

router = Router(name=__name__)


@router.callback_query(F.data == add_city)
async def weather_by_city(callback: CallbackQuery):

    await callback.message.answer(
        text='Enter the city name and its coordinates in the format: '
             'city name/latitude(N)/longitude(E)\n\n'
             'For example:\n'
             'New York/40.741406/-74.028346',
    )


@router.callback_query()
async def weather_by_location(callback: CallbackQuery):
    city, latitude, longitude = callback.data.split(sep='/')
    weather = await get_weather(latitude=latitude.strip(), longitude=longitude.strip())
    await callback.message.answer(
        text=f'The weather of {city.strip()}\n'
             f'elevation: <b>{weather['elevation']}m</b>\n'
             f'rain: <b>{weather['current']['rain']}{weather['current_units']['rain']}</b>\n'
             f'temperature: <b>{weather['current']['temperature_2m']}{weather['current_units']['temperature_2m']}</b>\n'
             f'precipitation: <b>{weather['current']['precipitation']}{weather['current_units']['precipitation']}</b>\n'
             f'humidity: <b>{weather['current']['relative_humidity_2m']}{weather['current_units']['relative_humidity_2m']}</b>\n'
             f'wind direction: <b>{weather['current']['wind_direction_10m']}{weather['current_units']['wind_direction_10m']}</b>\n'
             f'wind speed: <b>{weather['current']['wind_speed_10m']}{weather['current_units']['wind_speed_10m']}</b>',
        parse_mode=ParseMode.HTML,
    )
