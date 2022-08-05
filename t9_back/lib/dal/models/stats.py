import typing as t
from datetime import datetime

from sqlmodel import (
    Column,
    DateTime,
    Field,
    Relationship,
    SQLModel,
)

if t.TYPE_CHECKING:
    from .links import LinkModel, HitModel


class StatsModel(SQLModel, table=True):
    __tablename__ = "link_statistics"

    id: t.Optional[int] = Field(default=None, primary_key=True)
    hits: int = Field(default=0)
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow), nullable=False
    )

    link: "LinkModel" = Relationship(back_populates="stat")
    hit_count: t.List["HitModel"] = Relationship(back_populates="stats")
