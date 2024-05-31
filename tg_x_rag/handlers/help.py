from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

help_router = Router(name='help')

@help_router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer('HELP from TG_X_RAG!')