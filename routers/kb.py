import calendar
from datetime import date, timedelta

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from models import Location


def current_month() -> tuple[str, str]:
    """Returns first and last days of current month."""
    today: date = date.today()
    first_day: date = today.replace(day=1)
    last_day: date = date(
        year=today.year,
        month=today.month,
        day=calendar.monthrange(today.year, today.month)[1],
    )
    return first_day.strftime('%d.%m.%Y'), last_day.strftime('%d.%m.%Y')


def last_week() -> tuple[str, str]:
    """Returns week ago day and today."""
    today: date = date.today()
    seven_days_ago: date = date.today() - timedelta(days=7)
    return seven_days_ago.strftime('%d.%m.%Y'), today.strftime('%d.%m.%Y')


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
    first_day, last_day = current_month()

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='35₹ per liter (current month)',
            callback_data=f'liter=35\n{first_day}\n{last_day}',
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
    seven_days_ago, today = last_week()

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Current month',
            callback_data=f'{first_day}\n{last_day}',
        )],
        [InlineKeyboardButton(
            text='Last week',
            callback_data=f'{seven_days_ago}\n{today}',
        )],
    ])
