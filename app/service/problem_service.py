import random
from typing import List, Optional, Type

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.tag_crud import TagCRUD
from app.models import Problem, Tag


class ProblemService:
    def __init__(self, db: AsyncSession):
        self.db = db

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

        db_problem = Problem(
            contest_id=contest_id,
            index=index,
            name=name,
            category=category,
            points=points,
            solved_count=solved_count
        )

        self.db.add(db_problem)
        await self.db.flush()

        tag_crud = TagCRUD(self.db)

        if tags:
            for tag_name in tags:
                tag = await tag_crud.get_or_create(tag_name)
                db_problem.tags.append(tag)

        await self.db.commit()
        await self.db.refresh(db_problem)
        return db_problem

    async def get(self, contest_id: int, index: str) -> Optional[Problem]:
        result = await self.db.execute(
            select(Problem).filter_by(contest_id=contest_id, index=index)
        )
        return result.scalars().first()

    async def get_all(self) -> List[Type[Problem]]:
        result = await self.db.execute(select(Problem))
        return result.scalars().all()

    async def get_by_tag(self, tag_name: str) -> List[Type[Problem]]:
        result = await self.db.execute(
            select(Problem)
            .join(Problem.tags)
            .filter(Tag.name == tag_name)
        )
        return result.scalars().all()

    async def get_random_by_tag_and_points_range(
            self,
            tag_name: str,
            min_points: float,
            max_points: Optional[float] = None,
            limit: int = 10
    ) -> List[Problem]:
        conditions = [Tag.name == tag_name, Problem.points >= min_points]

        if max_points is not None:
            conditions.append(Problem.points <= max_points)

        result = await self.db.execute(
            select(Problem)
            .join(Problem.tags)
            .filter(and_(*conditions))
        )
        problems = result.scalars().all()
        random.shuffle(problems)
        return problems[:limit]
