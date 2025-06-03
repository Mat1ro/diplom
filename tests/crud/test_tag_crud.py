from unittest.mock import AsyncMock

import pytest

from app.crud.tag_crud import TagCRUD
from app.models import Tag


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def crud(mock_session):
    return TagCRUD(mock_session)


@pytest.mark.asyncio
async def test_get_by_name(crud):
    mock_tag = Tag(id=1, name="dp")
    crud.service.get_by_name = AsyncMock(return_value=mock_tag)

    result = await crud.get_by_name("dp")
    crud.service.get_by_name.assert_called_once_with("dp")
    assert result == mock_tag


@pytest.mark.asyncio
async def test_create(crud):
    mock_tag = Tag(id=2, name="graphs")
    crud.service.create = AsyncMock(return_value=mock_tag)

    result = await crud.create("graphs")
    crud.service.create.assert_called_once_with("graphs")
    assert result == mock_tag


@pytest.mark.asyncio
async def test_get_or_create(crud):
    mock_tag = Tag(id=3, name="math")
    crud.service.get_or_create = AsyncMock(return_value=mock_tag)

    result = await crud.get_or_create("math")
    crud.service.get_or_create.assert_called_once_with("math")
    assert result == mock_tag


@pytest.mark.asyncio
async def test_get_all(crud):
    mock_tags = [Tag(id=1, name="dp"), Tag(id=2, name="graphs")]
    crud.service.get_all = AsyncMock(return_value=mock_tags)

    result = await crud.get_all()
    crud.service.get_all.assert_called_once()
    assert result == mock_tags
