from rag.embedding import get_embeddings
from utils.config import DatabaseConfig, ModelConfig
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

async def query_model(text: str, include_documents: bool = True):
    db = Chroma(persist_directory=str(DatabaseConfig.CHROMA_PATH), embedding_function=get_embeddings())
    best_results = db.similarity_search_with_score(text, k=10)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in best_results])
    prompt_template = ChatPromptTemplate.from_template(ModelConfig.PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=text)
    model = Ollama(model=ModelConfig.MODEL_NAME)
    response = model.invoke(prompt)
    sources = [doc.metadata.get("id", None) for doc, _score in best_results]
    if include_documents:
        return response, sources
    return response, None