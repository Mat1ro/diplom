import requests

from app import database
from app.crud.problem_crud import ProblemCRUD
from app.models import Base


def fill():
    Base.metadata.drop_all(bind=database.engine)
    Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()

    res = requests.get("https://codeforces.com/api/problemset.problems")
    data = res.json()

    if data['status'] != 'OK':
        print("Ошибка при загрузке данных")
        return

    problems = data['result']['problems']
    stats = {(s['contestId'], s['index']): s['solvedCount'] for s in data['result']['problemStatistics']}

    problem_crud = ProblemCRUD(db)

    for problem in problems:
        contest_id = problem['contestId']
        index = problem['index']
        solved_count = stats.get((contest_id, index), 0)

        unique_tags = list(set(problem.get('tags', [])))

        problem_crud.create(
            contest_id=contest_id,
            index=index,
            name=problem['name'],
            category=problem.get('type', 'unknown'),
            points=problem.get('points'),
            solved_count=solved_count,
            tags=unique_tags
        )

    db.close()
    print("Загрузка завершена.")
