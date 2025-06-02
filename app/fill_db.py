import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Problem, Tag
from constants import DB_USER, PASSWORD, HOST, PORT, DATABASE

DATABASE_URL = f"postgresql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def fill_db_sync():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    res = requests.get("https://codeforces.com/api/problemset.problems")
    data = res.json()

    if data['status'] != 'OK':
        print("Ошибка при загрузке данных")
        return

    problems = data['result']['problems']
    stats = {(s['contestId'], s['index']): s['solvedCount'] for s in data['result']['problemStatistics']}

    for problem in problems:
        contest_id = problem['contestId']
        index = problem['index']
        solved_count = stats.get((contest_id, index), 0)
        unique_tags = list(set(problem.get('tags', [])))

        db_problem = Problem(
            contest_id=contest_id,
            index=index,
            name=problem['name'],
            category=problem.get('type', 'unknown'),
            points=problem.get('points'),
            solved_count=solved_count
        )
        session.add(db_problem)
        session.flush()

        for tag_name in unique_tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.flush()
            db_problem.tags.append(tag)

    session.commit()
    session.close()
    print("Заполнение БД завершено.")
