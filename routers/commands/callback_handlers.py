from re import Match

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from magic_filter import RegexpMode

from routers.kb import add_city
from services.milk import create_milk_sold_service
from utils import get_weather

router = Router(name=__name__)


@router.callback_query(F.data == add_city)
async def weather_by_city(callback: CallbackQuery):

    await callback.message.answer(
        text='Enter the city name and its coordinates.\n'
             '    city name\n'
             '    latitude(N)\n'
             '    longitude(E)\n\n'
             'For example:\n'
             '    New York\n'
             '    40.741406\n'
             '    -74.028346',
    )


@router.callback_query(
    F.data.regexp(
        r'^([A-Za-z\s]+)\n'
        r'(\d+(\.\d{1,2})?)\n'
        r'(\d+)$',
        mode=RegexpMode.MATCH,
    ).as_('sold'),
)
async def milk_sold_getter_callback(callback: CallbackQuery, sold: Match[str]):
    sale: str = sold.group()
    try:
        saved_sale = await create_milk_sold_service(sale=sale)
        await callback.message.answer(
            text='Your input has been saved as\n'
                 f'{saved_sale.name.name}\n'
                 f'{saved_sale.quantity} liters\n'
                 f'{saved_sale.price}',
        )
    except ValueError as e:
        await callback.message.answer(f'❌ {e}')


@router.callback_query()
async def weather_by_location(callback: CallbackQuery):
    city, latitude, longitude = callback.data.split(sep='/')
    weather = await get_weather(latitude=latitude, longitude=longitude)
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
