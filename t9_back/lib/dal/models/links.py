import typing as t
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship

from .common import Base
from .users import UserModel
from .stats import StatsModel


class LinkModel(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    stat_id = Column(Integer, ForeignKey("link_statistics.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    # updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    original_url = Column(String(512))
    short_url = Column(String(512))
    qr = Column(String(1024))

    user = relationship(UserModel, backref="links", foreign_keys=[user_id])
    stat = relationship(StatsModel, backref="links")


class HitModel(Base):
    __tablename__ = "link_hits"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    stat_id = Column(Integer, ForeignKey("link_statistics.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ip = Column(String(128))
    user_agent = Column(String(512))

    user = relationship(UserModel, backref="hits", foreign_keys=[user_id])
    stats = relationship(StatsModel, back_populates="hit_count")
