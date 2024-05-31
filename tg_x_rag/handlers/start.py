from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

start_router = Router(name='start')

@start_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Hello from TG_X_RAG!')