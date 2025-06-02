from typing import Type, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Tag


class TagService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Tag]:
        result = await self.session.execute(
            select(Tag).filter_by(name=name)
        )
        return result.scalars().first()

    async def create(self, name: str) -> Tag:
        tag = Tag(name=name)
        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)
        return tag

    async def get_or_create(self, name: str) -> Tag:
        tag = await self.get_by_name(name)
        if not tag:
            tag = await self.create(name)
        return tag

    async def get_all(self) -> List[Type[Tag]]:
        result = await self.session.execute(select(Tag))
        return result.scalars().all()
