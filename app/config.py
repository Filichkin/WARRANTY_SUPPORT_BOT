import os

from pydantic import SecretStr
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
    DEEPSEEK_MODEL_NAME: str = 'deepseek-chat'
    MISTRAL_MODEL_NAME: str = 'mistral-small-latest'
    DEEPSEEK_API_KEY: SecretStr
    MISTRAL_TOKEN: SecretStr
    ALGORITHM: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(
        env_file='/Users/alexeyfilichkin/MainDev/WARRANTY_SUPPORT_BOT/.env'
        )


settings = Config()
