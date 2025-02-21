from aiogram import Bot, Dispatcher

import asyncio
import logging

from .config import config


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=config.token)
    dp = Dispatcher()

    dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main=main())
