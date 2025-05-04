from typing import AsyncGenerator, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langchain_mistralai import ChatMistralAI
from loguru import logger

from app.config import settings


class ChatWithAI:
    """
    Класс для взаимодействия с различными языковыми моделями (LLM).
    Поддерживает работу с Mistral и Deepseek,
    с возможностью потокового вывода ответов.
    """

    def __init__(self, provider: Literal['deepseek', 'mistral'] = 'mistral'):
        """
        Инициализирует экземпляр класса с выбранным провайдером LLM.

        Args:
            provider (str):
            Провайдер языковой модели ('deepseek' или 'mistral')

        Raises:
            ValueError: Если указан неподдерживаемый провайдер
        """
        self.provider = provider

        if provider == 'deepseek':
            logger.info(
                f'Инициализация Deepseek модели: '
                f'{settings.DEEPSEEK_MODEL_NAME}'
                )
            self.llm = ChatDeepSeek(
                api_key=settings.DEEPSEEK_API_KEY,
                model=settings.DEEPSEEK_MODEL_NAME,
                temperature=0.0,
            )
        elif provider == 'mistral':
            logger.info(
                f'Инициализация Mistral модели: {settings.MISTRAL_MODEL_NAME}'
                )
            self.llm = ChatMistralAI(
                api_key=settings.MISTRAL_TOKEN,
                model=settings.MISTRAL_MODEL_NAME,
                temperature=0.0,
            )
        else:
            logger.error(f'Неподдерживаемый провайдер: {provider}')
            raise ValueError(f'Неподдерживаемый провайдер: {provider}')

        logger.success(f'Модель {provider} успешно инициализирована')

    async def astream_response(
        self, formatted_context: str, query: str
    ) -> AsyncGenerator[str, None]:
        """
        Асинхронно генерирует потоковый ответ от выбранной языковой модели.

        Args:
            formatted_context (str): Контекст из базы знаний,
            форматированный для запроса
            query (str): Пользовательский запрос

        Yields:
            str: Фрагменты ответа в потоковом режиме

        Notes:
            Использует системный промпт для задания контекста и роли модели
        """
        try:
            # Формируем системный промпт, определяющий роль
            # и контекст работы модели
            system_message = SystemMessage(
                content="""
                Ты — внутренний менеджер отдела гарантии.
                Отвечаешь по делу без лишних вступлений.
                Свой ответ, в первую очередь,
                ориентируй на переданный контекст.
                Если информации недостаточно - пробуй получить ответы
                из своей базы знаний.
                """
            )

            # Формируем пользовательский запрос с включенным контекстом
            human_message = HumanMessage(
                content=f'Вопрос: {query}\nКонтекст: '
                f'{formatted_context}. Ответ форматируй в markdown!'
            )

            logger.info(f'Начинаем стриминг ответа для запроса: «{query}»')

            # Асинхронно получаем фрагменты ответа
            async for chunk in self.llm.astream(
                [system_message, human_message]
            ):
                if chunk.content:  # Пропускаем пустые фрагменты
                    logger.debug(f'Получен фрагмент: {chunk.content[:50]}...')
                    yield chunk.content

            logger.info('Стриминг ответа успешно завершен')

        except Exception as e:
            logger.error(f'Ошибка при стриминге ответа: {e}')
            yield f'Произошла ошибка при обработке запроса: {str(e)}'
