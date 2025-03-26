from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='weather'), KeyboardButton(text='milk')],
        ],
        resize_keyboard=True,
        input_field_placeholder='Select item...'
    )


def milk_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='took'), KeyboardButton(text='sold')],
            [KeyboardButton(text='monthly report')],
        ],
        resize_keyboard=True,
        input_field_placeholder='Select item...'
    )
