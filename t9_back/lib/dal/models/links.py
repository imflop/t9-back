import typing as t
from datetime import datetime

from sqlmodel import (
    Column,
    DateTime,
    Field,
    Relationship,
    SQLModel,
)

from .users import UserModel
from .stats import StatsModel


class LinkModel(SQLModel, table=True):
    __tablename__ = "links"

    id: t.Optional[int] = Field(default=None, primary_key=True)
    stat_id: int = Field(foreign_key="link_statistics.id", index=True)
    user_id: t.Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow), nullable=False)
    original_url: str
    short_url: t.Optional[str]
    qr: t.Optional[str]

    user: t.Optional[UserModel] = Relationship(back_populates="links")
    stat: StatsModel = Relationship(back_populates="link")


class HitModel(SQLModel, table=True):
    __tablename__ = "link_hits"

    id: t.Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow), nullable=False)
    stat_id: int = Field(foreign_key="link_statistics.id", index=True)
    user_id: t.Optional[int] = Field(default=None, foreign_key="users.id")
    ip: str
    user_agent: str

    user: t.Optional[UserModel] = Relationship(back_populates="hits")
    stats: StatsModel = Relationship(back_populates="hit_count")
