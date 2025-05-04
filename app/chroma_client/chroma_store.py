from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger
import torch

from app.config import settings
from app.constants import SEARCH_COUNT


class ChromaVectorStore:
    def __init__(self):
        """
        Инициализирует пустой экземпляр хранилища векторов.
        Соединение с базой данных будет установлено позже
        с помощью метода init().
        """
        self._store: Chroma | None = None

    async def init(self):
        """
        Асинхронный метод для инициализации соединения с базой данных Chroma.
        Создает embeddings на основе модели из настроек,
        используя MPS если доступно.
        """
        logger.info('Инициализация ChromaVectorStore...')
        try:
            # Определяем устройство для вычислений:
            # GPU если доступен, иначе CPU
            device = 'mps' if torch.backends.mps.is_available() else 'cpu'
            logger.info(f'Используем устройство для эмбеддингов: {device}')

            # Создаем модель эмбеддингов с указанными параметрами
            embeddings = HuggingFaceEmbeddings(
                model_name=settings.LM_MODEL_NAME,
                model_kwargs={'device': device},
                encode_kwargs={'normalize_embeddings': True},
            )
            # Инициализируем соединение с базой данных Chroma
            self._store = Chroma(
                persist_directory=settings.CHROMA_PATH,
                embedding_function=embeddings,
                collection_name=settings.COLLECTION_NAME,
            )

            logger.success(
                f'ChromaVectorStore успешно подключен к коллекции '
                f'{settings.COLLECTION_NAME} в {settings.CHROMA_PATH}'
            )
        except Exception as e:
            logger.exception(
                f'Ошибка при инициализации ChromaVectorStore: {e}'
                )
            raise

    async def asimilarity_search(
            self,
            query: str,
            with_score: bool,
            k: int = SEARCH_COUNT
    ):
        """
        Асинхронный метод для поиска похожих документов в базе данных Chroma.

        Args:
            query (str): Текстовый запрос для поиска
            with_score (bool): Включать ли оценку релевантности в результаты
            k (int): Количество возвращаемых результатов

        Returns:
            list: Список найденных документов,
            возможно с оценками если with_score=True

        Raises:
            RuntimeError: Если хранилище не инициализировано
        """
        if not self._store:
            raise RuntimeError('ChromaVectorStore is not initialized.')

        logger.info(
            f'Поиск похожих документов по запросу: «{query}», top_k={k}'
            )
        try:
            if with_score:
                results = await self._store.asimilarity_search_with_score(
                    query=query, k=k
                )
            else:
                results = await self._store.asimilarity_search(
                    query=query,
                    k=k
                    )

            logger.debug(f'Найдено {len(results)} результатов.')
            return results
        except Exception as e:
            logger.exception(f'Ошибка при поиске: {e}')
            raise

    async def close(self):
        """
        Асинхронный метод для закрытия соединения с базой данных Chroma.
        В текущей реализации Chroma не требует явного закрытия,
        но метод добавлен для полноты API и возможных будущих изменений.
        """
        logger.info('Отключение ChromaVectorStore...')
        # Пока Chroma не требует явного закрытия,
        # но в будущем может понадобиться
        # self._store.close() или подобный метод
        pass


chroma_vectorstore = ChromaVectorStore()


def get_vectorstore() -> ChromaVectorStore:
    return chroma_vectorstore
