from typing import Optional

from sqlalchemy.orm import Session

from app.models import Tag
from app.service.tag_service import TagService


class TagCRUD:
    def __init__(self, session: Session):
        self.service = TagService(session)

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.service.get_by_name(name)

    def create(self, tag_name: str) -> Tag:
        return self.service.create(tag_name)

    def get_or_create(self, tag_name: str) -> Tag:
        return self.service.get_or_create(tag_name)

    def get_all(self):
        return self.service.get_all()
