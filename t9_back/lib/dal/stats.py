import dataclasses as dc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..dal.models.stats import StatsModel


@dc.dataclass(repr=False)
class StatsRepository:
    db: AsyncSession

    async def _store_model(self, stat: StatsModel) -> StatsModel:
        await self.db.commit()
        await self.db.refresh(stat)

        return stat

    async def save_stat_for_link(self, link_id: int) -> StatsModel:
        stat = StatsModel(link_id=link_id)
        self.db.add(stat)

        return await self._store_model(stat)

    async def increase_hit(self, stat_id: int) -> None:
        q = select(StatsModel).where(StatsModel.id == stat_id)
        result = await self.db.execute(q)

        if row := result.fetchone():
            stat = row[StatsModel]
            stat.hits += 1
            await self._store_model(stat)

