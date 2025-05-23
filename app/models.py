from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Many-to-many таблица связи
problem_tags = Table(
    'problem_tags',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Problem(Base):
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
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    problems = relationship('Problem', secondary=problem_tags, back_populates='tags')
