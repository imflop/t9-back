import pytest

from t9_back.lib.dal.links import LinkRepository

from ...factory_boys import LinkFactory, StatsFactory


@pytest.fixture()
def repository(db):
    return LinkRepository(db)


@pytest.mark.asyncio
async def test_get_link_is_none(repository):
    link = LinkFactory.build()
    data = await repository.get_link(link.id)
    assert data is None


@pytest.mark.asyncio
async def test_get_link(repository):
    link = LinkFactory.create(stat=StatsFactory.create())
    data = await repository.get_link(link.id)
    assert data == link


@pytest.mark.asyncio
async def test_save_link(repository, faker):
    lnk = faker.url()
    result = await repository.save_link(lnk)
    assert result.original_url == lnk
