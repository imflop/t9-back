import typing as t
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime
)
from sqlalchemy.orm import relationship

from .common import Base
from .links import LinkModel, HitModel


class StatsModel(Base):
    __tablename__ = "link_statistics"

    id = Column(Integer, primary_key=True)
    hits = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    link = relationship(LinkModel, backref="stat")
    hit_count = relationship(HitModel, backref="stats")
