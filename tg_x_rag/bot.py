import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.help import help_router
from handlers.start import start_router
from handlers.query import query_router
from handlers.rag_docs import rag_docs_router

async def main():
    load_dotenv()
    BOT_TOKEN = getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(start_router, help_router, query_router, rag_docs_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())