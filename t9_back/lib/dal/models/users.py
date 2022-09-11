from __future__ import annotations

import typing as t
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Boolean
)
from sqlalchemy.orm import relationship

from .common import Base

if t.TYPE_CHECKING:
    from .links import LinkModel
    from .stats import HitModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(256))
    salt = Column(String(256))
    password = Column(String(256))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    links = relationship(LinkModel, backref="user")
    hits = relationship(HitModel, backref="user")
