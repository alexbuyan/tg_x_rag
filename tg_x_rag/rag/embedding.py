from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def get_embeddings():
    embeddings = SentenceTransformerEmbeddings()
    return embeddings