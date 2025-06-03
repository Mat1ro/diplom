"""
Модуль CRUD операций для работы с задачами.

Этот модуль предоставляет интерфейс для работы с задачами в базе данных через слой сервисов.
"""

from typing import List, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Problem
from app.service.problem_service import ProblemService


class ProblemCRUD:
    """
    Класс для выполнения CRUD операций с задачами.
    
    Attributes:
        session (ProblemService): Сервис для работы с задачами
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация CRUD операций.
        
        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy
        """
        self.session = ProblemService(session)

    async def create(
            self,
            contest_id: int,
            index: str,
            name: str,
            category: str,
            points: Optional[float] = None,
            solved_count: int = 0,
            tags: List[str] = None
    ) -> Problem:
        """
        Создание новой задачи.
        
        Args:
            contest_id (int): ID контеста
            index (str): Индекс задачи
            name (str): Название задачи
            category (str): Категория задачи
            points (Optional[float]): Количество очков
            solved_count (int): Количество решений
            tags (List[str]): Список тегов
        
        Returns:
            Problem: Созданная задача
        """
        return await self.session.create(
            contest_id=contest_id,
            index=index,
            name=name,
            category=category,
            points=points,
            solved_count=solved_count,
            tags=tags
        )

    async def get(self, contest_id: int, index: str) -> Optional[Problem]:
        """
        Получение задачи по ID контеста и индексу.
        
        Args:
            contest_id (int): ID контеста
            index (str): Индекс задачи
        
        Returns:
            Optional[Problem]: Найденная задача или None
        """
        return await self.session.get(contest_id=contest_id, index=index)

    async def get_all(self) -> List[Type[Problem]]:
        """
        Получение всех задач.
        
        Returns:
            List[Problem]: Список всех задач
        """
        return await self.session.get_all()

    async def get_by_tag(self, tag_name: str) -> List[Type[Problem]]:
        """
        Получение задач по тегу.
        
        Args:
            tag_name (str): Название тега
        
        Returns:
            List[Problem]: Список задач с указанным тегом
        """
        return await self.session.get_by_tag(tag_name)

    async def get_random_by_tag_and_points_range(
            self,
            tag_name: str,
            min_points: float,
            max_points: Optional[float] = None,
            limit: int = 10
    ) -> List[Problem]:
        """
        Получение случайных задач по тегу и диапазону сложности.
        
        Args:
            tag_name (str): Название тега
            min_points (float): Минимальная сложность
            max_points (Optional[float]): Максимальная сложность
            limit (int): Максимальное количество задач
        
        Returns:
            List[Problem]: Список случайных задач
        """
        return await self.session.get_random_by_tag_and_points_range(
            tag_name, min_points, max_points, limit
        )
