from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
            [KeyboardButton(text='Monthly report')],
        ],
        resize_keyboard=True,
        input_field_placeholder='Select item...'
    )
