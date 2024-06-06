from pathlib import Path

class DatabaseConfig:
    DATA_PATH = Path.cwd() / 'data'
    CHROMA_PATH = Path.cwd() / 'chroma'

class ModelConfig:
    MODEL_NAME = 'llama3'

    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """