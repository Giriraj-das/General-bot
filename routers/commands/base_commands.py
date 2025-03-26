from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

from routers.kb import start_keyboard

router = Router(name=__name__)

IMAGE_URL = 'https://static.vecteezy.com/system/resources/previews/024/238/434/non_2x/ai-generated-small-robots-futuristic-marvels-of-artificial-intelligence-free-png.png'


@router.message(CommandStart())
async def handle_start(message: types.Message):
    text = markdown.text(
        f'{markdown.hide_link(IMAGE_URL)}Hello, {markdown.hbold(message.from_user.full_name)}!',
        "I'm your assistant bot. Choose what you want to do.",
        sep='\n',
    )
    await message.answer(
        text=text,
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.HTML
    )


@router.message(Command('help'))
async def handle_help(message: types.Message):
    text = markdown.text(
        f'{markdown.hide_link(IMAGE_URL)}Hello, {markdown.hbold(message.from_user.full_name)}!',
        "I'm your assistant bot. Select on the keyboard what you want to do.",
        sep='\n',
    )
    await message.answer(
        text=text,
        reply_markup=start_keyboard(),
        parse_mode=ParseMode.HTML,
    )
