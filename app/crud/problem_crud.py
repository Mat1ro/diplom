from typing import List, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Problem
from app.service.problem_service import ProblemService


class ProblemCRUD:
    def __init__(self, session: AsyncSession):
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
        return await self.session.get(contest_id=contest_id, index=index)

    async def get_all(self) -> List[Type[Problem]]:
        return await self.session.get_all()

    async def get_by_tag(self, tag_name: str) -> List[Type[Problem]]:
        return await self.session.get_by_tag(tag_name)

    async def get_random_by_tag_and_points_range(
            self,
            tag_name: str,
            min_points: float,
            max_points: Optional[float] = None,
            limit: int = 10
    ) -> List[Problem]:
        return await self.session.get_random_by_tag_and_points_range(
            tag_name, min_points, max_points, limit
        )
