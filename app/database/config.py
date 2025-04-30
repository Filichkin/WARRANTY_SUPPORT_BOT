import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    PARSED_JSON_PATH: str = os.path.join(BASE_DIR, 'data', 'JSON')
    CHROMA_PATH: str = os.path.join(BASE_DIR, 'chroma_db')
    COLLECTION_NAME: str = 'warranty_data'
    MAX_CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    LM_MODEL_NAME: str = (
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        )


settings = Config()
