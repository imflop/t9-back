import dataclasses as dc
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models.stats import StatsModel
from ..dal.models.links import LinkModel, HitModel


ModelFilter = t.Union[LinkModel, HitModel]


@dc.dataclass(repr=False)
class LinkRepository:
    db: AsyncSession

    # see: https://github.com/tiangolo/sqlmodel/issues/189
    # def get_link(self, link_filter: int) -> t.Optional[LinkModel]:
    #     stmt = select(LinkModel).where(LinkModel.id == link_filter)
    #     return self.db.exec(stmt).first()

    async def get_link(self, link_filter: int) -> t.Optional[LinkModel]:
        q = select(LinkModel, StatsModel, HitModel)\
            .join(StatsModel, LinkModel.stat_id == StatsModel.id)\
            .join(HitModel, HitModel.stat_id == StatsModel.id)\
            .options(selectinload(LinkModel.stat), selectinload(StatsModel.hit_count), selectinload(StatsModel.link))\
            .where(LinkModel.id == link_filter)
        # stmt = select(LinkModel, StatsModel).select_from(
        #     join(LinkModel, StatsModel, LinkModel.stat)
        #     # .join(HitModel, StatsModel, HitModel.stats)
        # ).where(LinkModel.id == link_filter)
        result = await self.db.execute(q)
        # result = await self.db.execute(stmt)
        row = result.fetchone()

        return row[LinkModel] if row else None

    async def _store_model(self, model_filter: ModelFilter) -> ModelFilter:
        await self.db.commit()
        await self.db.refresh(model_filter)

        return model_filter

    async def save_link(self, original_url: str) -> LinkModel:
        stat = StatsModel()
        link = LinkModel(original_url=original_url, stat=stat)
        self.db.add(link)

        return await self._store_model(link)

    async def save_hit(self, link: LinkModel, ip: str, user_agent: str) -> HitModel:
        hit = HitModel(
            stat_id=link.stat_id,
            ip=ip,
            user_agent=user_agent
        )
        self.db.add(hit)

        return await self._store_model(hit)

    async def upsert_link(self, link: LinkModel) -> LinkModel:
        await self.db.merge(link)

        return await self._store_model(link)
