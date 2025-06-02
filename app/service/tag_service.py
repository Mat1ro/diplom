"""
Модуль сервисного слоя для работы с тегами.

Этот модуль предоставляет бизнес-логику для работы с тегами в базе данных.
"""

from typing import Type, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Tag


class TagService:
    """
    Сервис для работы с тегами.
    
    Attributes:
        session (AsyncSession): Асинхронная сессия SQLAlchemy
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса.
        
        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy
        """
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Tag]:
        """
        Получение тега по названию.
        
        Args:
            name (str): Название тега
        
        Returns:
            Optional[Tag]: Найденный тег или None
        """
        result = await self.session.execute(
            select(Tag).filter_by(name=name)
        )
        return result.scalars().first()

    async def create(self, name: str) -> Tag:
        """
        Создание нового тега.
        
        Args:
            name (str): Название тега
        
        Returns:
            Tag: Созданный тег
        """
        tag = Tag(name=name)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def get_or_create(self, name: str) -> Tag:
        """
        Получение существующего тега или создание нового.
        
        Args:
            name (str): Название тега
        
        Returns:
            Tag: Найденный или созданный тег
        """
        tag = await self.get_by_name(name)
        if not tag:
            tag = await self.create(name)
        return tag

    async def get_all(self) -> List[Type[Tag]]:
        """
        Получение всех тегов.
        
        Returns:
            List[Tag]: Список всех тегов
        """
        result = await self.session.execute(select(Tag))
        return result.scalars().all()
