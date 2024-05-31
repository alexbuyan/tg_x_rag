from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from rag.database import clear_database
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from rag.database import load_docs, split_docs, update_database
from utils.config import DatabaseConfig

rag_docs_router = Router(name='rag_docs')

class LoadDoc(StatesGroup):
    provide_doc = State()

@rag_docs_router.message(Command('load_doc'))
async def load_docs_handler(message: Message, state: FSMContext):
    await message.answer('Please load the PDF document that you want to add to RAG context:')
    await state.set_state(LoadDoc.provide_doc)

@rag_docs_router.message(LoadDoc.provide_doc, F.document)
async def upload_provided_doc_handler(message: Message, bot: Bot):
    document = message.document
    file_name = message.document.file_name
    destination = DatabaseConfig.DATA_PATH / file_name
    await bot.download(file=document, destination=destination)
    documents = load_docs()
    chunks = split_docs(documents)
    update_database(chunks)
    await message.answer('File has been uploaded!')

@rag_docs_router.message(Command('clear_docs'))
async def clear_docs_handler(message: Message):
    await clear_database()
    await message.answer('All the documents in the RAG context were cleared!')