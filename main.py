import logging
import os

import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.commands import start, help, top
from utils.managers.db_manager import create_table

# Initialize MemoryStorage
storage = MemoryStorage()

load_dotenv()

BOT_TOKEN = os.getenv('token')

async def main():
    await create_table() # Create SQL table in runing bot
    # Initialize bot and dispatcher with MemoryStorage
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)
    # Register Routes
    dp.include_routers(start.router, help.router, top.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    logging.info('Bot has been started')
