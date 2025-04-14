import calendar
from datetime import date

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from models import Location


def current_month():
    """Returns first and last days of current month."""
    today: date = date.today()
    first_day: date = today.replace(day=1)
    last_day: date = date(
        year=today.year,
        month=today.month,
        day=calendar.monthrange(today.year, today.month)[1],
    )
    return first_day, last_day


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Weather'), KeyboardButton(text='Milk')],
        ],
        resize_keyboard=True,
        input_field_placeholder='Select item...'
    )


def milk_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Took'), KeyboardButton(text='Sold')],
            [KeyboardButton(text='Supplies report'), KeyboardButton(text='Sales report by name')],
            [KeyboardButton(text='General report')],
        ],
        resize_keyboard=True,
        input_field_placeholder='Select item...'
    )


def cities_keyboard(locations: list[Location]) -> InlineKeyboardMarkup:
    rows = []
    for location in locations:
        rows.append([InlineKeyboardButton(
            text=location.city,
            callback_data=f'{location.city}/{location.latitude}/{location.longitude}',
        )])

    rows.append([InlineKeyboardButton(
        text=f'➕ Add a city',
        callback_data='add_city',
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def sales_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Murari Mohini (1l 100r today)',
            callback_data='Murari Mohini\n1\n100',
        )],
        [InlineKeyboardButton(
            text='Indians (1l 100r today)',
            callback_data='Indians\n1\n100',
        )],
        [InlineKeyboardButton(
            text='Achyuta Dharma (1l 100r today)',
            callback_data='Achyuta Dharma\n1\n100',
        )],
    ])


def supplies_report_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='35₹ per liter',
            callback_data='liter=35',
        )],
    ])


def sales_report_by_name_keyboard() -> InlineKeyboardMarkup:
    first_day, last_day = current_month()

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Our milk (current month)',
            callback_data=f'For myself\n{first_day}\n{last_day}',
        )],
        [InlineKeyboardButton(
            text='Donation (current month)',
            callback_data=f'Donation\n{first_day}\n{last_day}',
        )],
        [InlineKeyboardButton(
            text='Murari Mohini (current month)',
            callback_data=f'Murari Mohini\n{first_day}\n{last_day}',
        )],
    ])


def general_report_keyboard() -> InlineKeyboardMarkup:
    first_day, last_day = current_month()

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Current month',
            callback_data=f'{first_day}\n{last_day}',
        )],
    ])
