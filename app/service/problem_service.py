from typing import List, Optional, Type

from sqlalchemy.orm import Session

from app.crud.tag_crud import TagCRUD
from app.models import Problem, Tag


class ProblemService:
    def __init__(self, db: Session):
        self.db = db

    def create(
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
        self.db.flush()

        tag_crud = TagCRUD(self.db)

        if tags:
            for tag_name in tags:
                tag = tag_crud.get_or_create(tag_name)
                db_problem.tags.append(tag)

        self.db.commit()
        self.db.refresh(db_problem)
        return db_problem

    def get(self, contest_id: int, index: str) -> Optional[Problem]:
        return self.db.query(Problem).filter(
            Problem.contest_id == contest_id,
            Problem.index == index
        ).first()

    def get_all(self) -> List[Type[Problem]]:
        return self.db.query(Problem).all()

    def get_by_tag(self, tag_name: str) -> List[Type[Problem]]:
        return (
            self.db
            .query(Problem)
            .join(Problem.tags)
            .filter(Tag.name == tag_name)
            .all()
        )
