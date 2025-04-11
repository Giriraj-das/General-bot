import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from routers import router as main_router


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=f'{settings.base_webhook_url}{settings.webhook_path}',
        secret_token=settings.webhook_secret,
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()
    logging.info('Webhook removed')


def main():
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    bot = Bot(
        token=settings.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    app = web.Application()
    handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.webhook_secret,
    )
    handler.register(app, path=settings.webhook_path)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=settings.run.host, port=settings.run.port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
