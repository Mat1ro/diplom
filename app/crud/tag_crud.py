from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Tag
from app.service.tag_service import TagService


class TagCRUD:
    def __init__(self, session: AsyncSession):
        self.service = TagService(session)

    async def get_by_name(self, name: str) -> Optional[Tag]:
        return await self.service.get_by_name(name)

    async def create(self, tag_name: str) -> Tag:
        return await self.service.create(tag_name)

    async def get_or_create(self, tag_name: str) -> Tag:
        return await self.service.get_or_create(tag_name)

    async def get_all(self):
        return await self.service.get_all()
