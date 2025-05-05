import time

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger

import torch

from pdf_text_splitter import load_documents


CHROMA_PATH = './warranty_chroma_db'
COLLECTION_NAME = 'warranty_data'
DOCUMENT_PATH = './data/warranty_policy.pdf'


def generate_chroma_db():
    try:
        start_time = time.time()

        logger.info('Загрузка модели эмбеддингов...')
        embeddings = HuggingFaceEmbeddings(
            model_name=(
                'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
                ),
            model_kwargs={
                'device': 'mps' if torch.backends.mps.is_available() else 'cpu'
                },
            encode_kwargs={'normalize_embeddings': True},
        )
        logger.info(f'Модель загружена за {time.time() - start_time:.2f} сек')

        logger.info('Создание Chroma DB...')
        chroma_db = Chroma.from_documents(
            documents=load_documents(DOCUMENT_PATH),
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name=COLLECTION_NAME,
        )
        logger.info(f'Chroma DB создана за {time.time() - start_time:.2f} сек')

        return chroma_db
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        raise


if __name__ == '__main__':
    generate_chroma_db()
