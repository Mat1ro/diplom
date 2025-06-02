"""
Модуль определения моделей базы данных.

Этот модуль содержит SQLAlchemy модели для работы с задачами Codeforces и их тегами.
"""

from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Таблица связи many-to-many между задачами и тегами
problem_tags = Table(
    'problem_tags',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Problem(Base):
    """
    Модель задачи Codeforces.
    
    Атрибуты:
        id (int): Уникальный идентификатор задачи
        contest_id (int): ID контеста
        index (str): Индекс задачи в контесте (например, 'A', 'B', 'C1')
        name (str): Название задачи
        category (str): Категория задачи
        points (float): Количество очков за задачу (может быть null)
        solved_count (int): Количество решений задачи
        tags (list[Tag]): Список тегов, связанных с задачей
    """
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contest_id = Column(Integer)
    index = Column(String)
    name = Column(String)
    category = Column(String)
    points = Column(Float, nullable=True)
    solved_count = Column(Integer, default=0)

    tags = relationship('Tag', secondary=problem_tags, back_populates='problems')


class Tag(Base):
    """
    Модель тега для задач Codeforces.
    
    Атрибуты:
        id (int): Уникальный идентификатор тега
        name (str): Название тега
        problems (list[Problem]): Список задач, связанных с тегом
    """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    problems = relationship('Problem', secondary=problem_tags, back_populates='tags')
