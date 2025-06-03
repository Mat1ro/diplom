from unittest.mock import AsyncMock

import pytest

from app.crud.problem_crud import ProblemCRUD
from app.models import Problem


@pytest.fixture
def mock_session():
    # просто заглушка для AsyncSession
    return AsyncMock()


@pytest.fixture
def crud(mock_session):
    return ProblemCRUD(mock_session)


@pytest.mark.asyncio
async def test_create(crud):
    # Мокаем метод create у ProblemService
    crud.session.create = AsyncMock(return_value=Problem(id=1, name="Test Problem"))

    result = await crud.create(
        contest_id=1,
        index="A",
        name="Test Problem",
        category="Algorithms",
        points=100,
        solved_count=0,
        tags=["dp"]
    )
    crud.session.create.assert_called_once_with(
        contest_id=1,
        index="A",
        name="Test Problem",
        category="Algorithms",
        points=100,
        solved_count=0,
        tags=["dp"]
    )
    assert isinstance(result, Problem)
    assert result.name == "Test Problem"


@pytest.mark.asyncio
async def test_get(crud):
    crud.session.get = AsyncMock(return_value=Problem(id=1, name="Test Problem"))

    result = await crud.get(contest_id=1, index="A")
    crud.session.get.assert_called_once_with(contest_id=1, index="A")
    assert isinstance(result, Problem)
    assert result.name == "Test Problem"


@pytest.mark.asyncio
async def test_get_all(crud):
    crud.session.get_all = AsyncMock(return_value=[Problem(id=1), Problem(id=2)])

    result = await crud.get_all()
    crud.session.get_all.assert_called_once()
    assert isinstance(result, list)
    assert all(isinstance(p, Problem) for p in result)


@pytest.mark.asyncio
async def test_get_by_tag(crud):
    crud.session.get_by_tag = AsyncMock(return_value=[Problem(id=1)])

    result = await crud.get_by_tag("dp")
    crud.session.get_by_tag.assert_called_once_with("dp")
    assert isinstance(result, list)
    assert all(isinstance(p, Problem) for p in result)


@pytest.mark.asyncio
async def test_get_random_by_tag_and_points_range(crud):
    crud.session.get_random_by_tag_and_points_range = AsyncMock(return_value=[Problem(id=1)])

    result = await crud.get_random_by_tag_and_points_range("dp", 50, 100, 5)
    crud.session.get_random_by_tag_and_points_range.assert_called_once_with("dp", 50, 100, 5)
    assert isinstance(result, list)
    assert all(isinstance(p, Problem) for p in result)
