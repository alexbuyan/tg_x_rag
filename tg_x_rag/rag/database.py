import os
import shutil
from h11 import Data
from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from rag.embedding import get_embeddings
from utils.config import DatabaseConfig

def load_docs():
    document_loader = PyPDFDirectoryLoader(str(DatabaseConfig.DATA_PATH))
    return document_loader.load()

def split_docs(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        is_separator_regex=False
    )
    return text_splitter.split_documents(docs)

def update_database(chunks: list[Document]):
    db = Chroma(persist_directory=str(DatabaseConfig.CHROMA_PATH), embedding_function=get_embeddings())
    chunks_with_ids = assign_chunk_ids(chunks)
    existing_chunks = db.get(include=[])
    existing_ids = set(existing_chunks['ids'])
    new_chunks = []
    new_chunk_ids = []
    for chunk in chunks_with_ids:
        if chunk.metadata['id'] not in existing_ids:
            new_chunks.append(chunk)
            new_chunk_ids.append(chunk.metadata['id'])

    if len(new_chunks) != 0:
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
        return True
    return False
    

def assign_chunk_ids(chunks):
    last_page_id = None
    curr_chunk_id = 0
    for chunk in chunks:
        source = chunk.metadata.get('source')
        page = chunk.metadata.get('page')
        curr_page_id = f'{source}:{page}'
        if curr_page_id == last_page_id:
            curr_chunk_id += 1
        else:
            curr_chunk_id = 0

        chunk_id = f'page:{curr_page_id}_chunk:{curr_chunk_id}'
        last_page_id = curr_page_id
        chunk.metadata['id'] = chunk_id
    return chunks

async def clear_database():
    if DatabaseConfig.CHROMA_PATH.exists():
        shutil.rmtree(str(DatabaseConfig.CHROMA_PATH))
    if DatabaseConfig.DATA_PATH.exists():
        shutil.rmtree(str(DatabaseConfig.DATA_PATH))
    os.mkdir(str(DatabaseConfig.DATA_PATH))
