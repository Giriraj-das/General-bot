from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from models import Location

add_city = 'add_city'


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

    rows.append([InlineKeyboardButton(text=f'➕ Add a city', callback_data=add_city)])
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
