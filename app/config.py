import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    PARSED_JSON_PATH: str = os.path.join(
        BASE_DIR,
        'database_utils',
        'data', 'JSON'
        )
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
    JWT_REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str

    model_config = SettingsConfigDict()


settings = Config()


def get_db_url():
    return (f'postgresql+asyncpg://{settings.POSTGRES_USER}:'
            f'{settings.POSTGRES_PASSWORD}@'
            f'{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/'
            f'{settings.POSTGRES_DB}'
            )


def get_auth_data():
    return {
        'secret_key': settings.SECRET_KEY,
        'jwt_refresh_secret_key': settings.JWT_REFRESH_SECRET_KEY,
        'algorithm': settings.ALGORITHM,
        'acces_token_expire_minutes': settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        'refresh_token_expire_minutes': settings.REFRESH_TOKEN_EXPIRE_MINUTES
        }
