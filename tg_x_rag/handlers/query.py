import os
from typing import Any, Dict
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from rag.query import query_model
from aiogram.types import ReplyKeyboardRemove

from utils.keyboards import yes_no_keyboard
from utils.config import DatabaseConfig

query_router = Router(name='query')

class Query(StatesGroup):
    on_first = State()
    inc_docs = State()
    query_text = State()
    

@query_router.message(Command('chat'))
async def query_handler(message: Message, state: FSMContext):
    if os.listdir(str(DatabaseConfig.DATA_PATH)) == []:
        return await message.answer('Please upload the documents first using /load_doc command!')
    
    await state.set_state(Query.inc_docs)
    await state.update_data(on_first=True)
    await message.answer(
        'Should we include the sources to the response?', 
        reply_markup=yes_no_keyboard(),
    )

@query_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        "Chat has been cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

@query_router.message(Query.inc_docs)
async def process_include_docs(message: Message, state: FSMContext):
    data = await state.get_data()
    on_first = data['on_first']
    print(on_first)

    if on_first == True:
        print('here')
        option = message.text
        print(option)
        if option == 'yes':
            await state.update_data(include_documents=True)
        elif option == 'no':
            await state.update_data(include_documents=False)
        else:
            await message.answer('Please choose one of the options provided below:', reply_markup=yes_no_keyboard())
            return

    await state.set_state(Query.query_text)
    await message.answer('Please specify your query to the RAG model.\n\nTo stop the chat use /cancel command.', reply_markup=ReplyKeyboardRemove())


@query_router.message(Query.query_text)
async def process_query_text(message: Message, state: FSMContext):
    await state.update_data(on_first=False)
    await state.update_data(query_text=message.text)
    await message.answer('Processing the query, please wait...')
    data = await state.get_data()
    await query_answer_handler(message, data)


async def query_answer_handler(message: Message, data: Dict[str, Any]):
    query = data['query_text']
    include_documents = data['include_documents']
    response, sources = await query_model(query, include_documents)
    await message.answer(response)
    if sources is not None:
        cleared_sources = []
        for source in sources:
            cleared_source = source.split('/')[-1]
            cleared_sources.append(cleared_source)
        sources_message = ',\n'.join(cleared_sources)
        await message.answer(f'The information was specified in these sources:\n{sources_message}')