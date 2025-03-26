from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown

router = Router()


@router.message(CommandStart())
async def handle_start(message: types.Message):
    url = 'https://static.vecteezy.com/system/resources/previews/024/238/434/non_2x/ai-generated-small-robots-futuristic-marvels-of-artificial-intelligence-free-png.png'
    await message.answer(
        text=f'{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!',
    )


@router.message(Command('help'))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm echo bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.underline("any"),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep='\n',
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
