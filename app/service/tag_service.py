from typing import Type, List, Optional

from sqlalchemy.orm import Session

from app.models import Tag


class TagService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.session.query(Tag).filter(Tag.name == name).first()

    def create(self, name: str) -> Tag:
        tag = Tag(name=name)
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def get_or_create(self, name: str) -> Tag:
        tag = self.get_by_name(name)
        if not tag:
            tag = self.create(name)
        return tag

    def get_all(self) -> List[Type[Tag]]:
        return self.session.query(Tag).all()
