import os
from typing import Any, Dict
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from rag.query import query_model
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from utils.config import DatabaseConfig

query_router = Router(name='query')

class Query(StatesGroup):
    before_query = State()
    query_text = State()
    include_documents = State()

@query_router.message(Command('chat'))
async def query_handler(message: Message, state: FSMContext):
    if os.listdir(str(DatabaseConfig.DATA_PATH)) == []:
        return await message.answer('Please upload the documents first using /load_doc command!')
    
    await state.set_state(Query.include_documents)
    await message.answer(
        'Should we include the sources to the response?', 
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='yes'),
                    KeyboardButton(text='no')
                ]
            ],
            resize_keyboard=True
        ),
    )

@query_router.message(Query.before_query)
async def before_query_handler(message: Message, state: FSMContext, on_first: bool = True):
    if on_first:
        await message.answer('Please provide the query for RAG model:')
    await state.set_state(Query.query_text)

@query_router.message(Query.query_text)
async def query_text_handler(message: Message, state: FSMContext):
    await state.update_data(query_text=message.text)
    data = await state.get_data()
    await message.answer('Processing the query, please wait...')
    await query_answer_handler(message, data)
    await before_query_handler(message, state, on_first=False)


@query_router.message(Query.include_documents, F.text.casefold() == 'yes')
async def process_include_docs(message: Message, state: FSMContext):
    await state.update_data(include_documents=True)
    await message.answer('Ok, I will include the sources!', reply_markup=ReplyKeyboardRemove())
    await before_query_handler(message, state)


@query_router.message(Query.include_documents, F.text.casefold() == 'no')
async def process_dont_include_docs(message: Message, state: FSMContext):
    await state.update_data(include_documents=False)
    await message.answer('Fine, I will write responses without the sources!', reply_markup=ReplyKeyboardRemove())
    await before_query_handler(message, state)

async def query_answer_handler(message: Message, data: Dict[str, Any]):
    query = data['query_text']
    include_documents = data['include_documents']
    response, sources = await query_model(query, include_documents)
    await message.answer('Here is the response from RAG Model!')
    await message.answer(response)
    if sources is not None:
        await message.answer('The information was specified in these sources:')
        sources_message = ',\n'.join(sources)
        await message.answer(sources_message)
