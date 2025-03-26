from aiogram import Router, types, F

from app.kb import milk_keyboard

router = Router(name=__name__)


@router.message(F.text == 'milk')
async def handle_help(message: types.Message):
    await message.answer(
        text='Select item',
        reply_markup=milk_keyboard(),
    )


@router.message(F.text == 'weather')
async def handle_help(message: types.Message):
    await message.answer(
        text='Select a city or add it (name and coordinates).',
    )
