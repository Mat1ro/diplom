"""
Модуль для заполнения базы данных данными с Codeforces API.

Этот модуль отвечает за:
1. Получение данных о задачах с Codeforces API
2. Создание и обновление таблиц в базе данных
3. Заполнение базы данных информацией о задачах и тегах
"""

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Problem, Tag
from constants import DB_USER, PASSWORD, HOST, PORT, DATABASE

# URL для подключения к базе данных
DATABASE_URL = f"postgresql://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Создание синхронного движка SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def fill_db_sync():
    """
    Синхронная функция для заполнения базы данных.
    
    Процесс:
    1. Удаляет все существующие таблицы
    2. Создает новые таблицы
    3. Получает данные о задачах с Codeforces API
    4. Заполняет базу данных задачами и тегами
    5. Связывает задачи с соответствующими тегами
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    # Получение данных с Codeforces API
    res = requests.get("https://codeforces.com/api/problemset.problems")
    data = res.json()

    if data['status'] != 'OK':
        print("Ошибка при загрузке данных")
        return

    problems = data['result']['problems']
    # Создание словаря статистики решений задач
    stats = {(s['contestId'], s['index']): s['solvedCount'] for s in data['result']['problemStatistics']}

    for problem in problems:
        contest_id = problem['contestId']
        index = problem['index']
        solved_count = stats.get((contest_id, index), 0)
        unique_tags = list(set(problem.get('tags', [])))

        # Создание объекта задачи
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

        # Добавление тегов к задаче
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
