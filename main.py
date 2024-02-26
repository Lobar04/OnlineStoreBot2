from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
import asyncio
import logging

from handlers.command_handler import command_router
from handlers.product_handlers import product_router


async def main():

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(command_router,product_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped!')

