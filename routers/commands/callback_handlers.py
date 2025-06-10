from re import Match

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from magic_filter import RegexpMode

from models import Sale
from services.milk import (
    create_milk_sold_service,
    get_supplies_between_dates_service,
    get_supplies_by_buyer_name_between_dates_service, supplies_general_report_service,
)
from utils import get_weather

router = Router(name=__name__)


@router.callback_query(F.data == 'add_city')
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
        r'^([A-Za-z ]+)\n'
        r'(\d+(\.\d{1,2})?)\n'
        r'(\d+)$',
        mode=RegexpMode.MATCH,
    ).as_('match'),
)
async def milk_sold_getter_callback(callback: CallbackQuery, match: Match[str]):
    try:
        saved_sale: Sale = await create_milk_sold_service(match=match)
        await callback.message.answer(
            text='Your input has been saved as\n'
                 f'{saved_sale.name.name}\n'
                 f'{saved_sale.quantity} liters\n'
                 f'{saved_sale.price}',
        )
    except ValueError as e:
        await callback.message.answer(f'❌ {e}')


@router.callback_query(
    F.data.regexp(
        r'^(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('dates')
)
async def supplies_general_report_callback(callback: CallbackQuery, dates: Match[str]):
    text_blocks: list[str] = await supplies_general_report_service(
        start_date=dates.group(1),
        end_date=dates.group(2),
    )
    for block in text_blocks:
        await callback.message.answer(text=block)


@router.callback_query(
    F.data.regexp(
        r'^([a-zA-Z ]+)\n'
        r'(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('match')
)
async def supplies_report_by_buyer_name_between_dates_callback(callback: CallbackQuery, match: Match[str]):
    text_blocks: list[str] = await get_supplies_by_buyer_name_between_dates_service(
        name_part=match.group(1),
        start_date=match.group(2),
        end_date=match.group(3),
    )
    for block in text_blocks:
        await callback.message.answer(text=block)


@router.callback_query(
    F.data.regexp(
        r'^[Ll]iter=(\d+)\n'
        r'(\d{2}\.\d{2}\.\d{4})\n'
        r'(\d{2}\.\d{2}\.\d{4})$',
        mode=RegexpMode.MATCH,
    ).as_('match')
)
async def supplies_report_between_dates_callback(callback: CallbackQuery, match: Match[str]):
    text_blocks: list[str] = await get_supplies_between_dates_service(
        price=int(match.group(1)),
        start_date=match.group(2),
        end_date=match.group(3),
    )
    for block in text_blocks:
        await callback.message.answer(text=block)


@router.callback_query(
    F.data.regexp(
        r'^([a-zA-Z ]+)/(-?\d+\.\d+)/(-?\d+\.\d+)$',
        mode=RegexpMode.MATCH,
    ).as_('match'),
)
async def weather_by_location_callback(callback: CallbackQuery, match: Match[str]):
    city, latitude, longitude = match.group(1), match.group(2), match.group(3)
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
