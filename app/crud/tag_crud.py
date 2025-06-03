"""
Модуль CRUD операций для работы с тегами.

Этот модуль предоставляет интерфейс для работы с тегами в базе данных через слой сервисов.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag
from app.service.tag_service import TagService


class TagCRUD:
    """
    Класс для выполнения CRUD операций с тегами.
    
    Attributes:
        service (TagService): Сервис для работы с тегами
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация CRUD операций.
        
        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy
        """
        self.service = TagService(session)

    async def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Получение тега по названию.
        
        Args:
            name (str): Название тега
        
        Returns:
            Optional[Tag]: Найденный тег или None
        """
        return await self.service.get_by_name(name)

    async def create(self, tag_name: str) -> Tag:
        """
        Создание нового тега.
        
        Args:
            tag_name (str): Название тега
        
        Returns:
            Tag: Созданный тег
        """
        return await self.service.create(tag_name)

    async def get_or_create(self, tag_name: str) -> Tag:
        """
        Получение существующего тега или создание нового.
        
        Args:
            tag_name (str): Название тега
        
        Returns:
            Tag: Найденный или созданный тег
        """
        return await self.service.get_or_create(tag_name)

    async def get_all(self):
        """
        Получение всех тегов.
        
        Returns:
            List[Tag]: Список всех тегов
        """
        return await self.service.get_all()
