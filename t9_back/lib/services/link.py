import dataclasses as dc

from ..dal.links import LinkRepository
from ..dal.stats import StatsRepository
from ..dal.models.links import LinkModel, HitModel
from ..serializers.link import Link, LinkIn


@dc.dataclass(repr=False, slots=True)
class LinkService:
    link_repository: LinkRepository
    stat_repository: StatsRepository

    async def get_link(self, link_filter: int) -> LinkModel:
        return await self.link_repository.get_link(link_filter)

    async def save_link(self, new_link: LinkIn) -> LinkModel:
        return await self.link_repository.save_link(new_link.original_url)

    async def update_link(self, link: LinkModel) -> Link:
        link_model = await self.link_repository.upsert_link(link)

        return Link.from_orm(link_model)

    async def increase_hit_count(self, link: LinkModel, ip: str, user_agent: str) -> HitModel:
        hit = await self.link_repository.save_hit(link, ip, user_agent)
        await self.stat_repository.increase_hit(hit.stat_id)

        return hit
