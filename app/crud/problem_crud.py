from typing import List, Optional, Type

from sqlalchemy.orm import Session

from app.models import Problem
from app.service.problem_service import ProblemService


class ProblemCRUD:
    def __init__(self, session: Session):
        self.session = ProblemService(session)

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
        return self.session.create(
            contest_id=contest_id,
            index=index,
            name=name,
            category=category,
            points=points,
            solved_count=solved_count,
            tags=tags
        )

    def get(self, contest_id: int, index: str) -> Optional[Problem]:
        return self.session.get(contest_id=contest_id, index=index)

    def get_all(self) -> List[Type[Problem]]:
        return self.session.get_all()

    def get_by_tag(self, tag_name: str) -> List[Type[Problem]]:
        return self.session.get_by_tag(tag_name)
