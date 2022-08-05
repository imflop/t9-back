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
    from .links import LinkModel
    from .stats import HitModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: t.Optional[int] = Field(default=None, primary_key=True)
    email: str
    salt: str
    password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.utcnow), nullable=False)
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow), nullable=False
    )

    links: t.List["LinkModel"] = Relationship(back_populates="user")
    hits: t.List["HitModel"] = Relationship(back_populates="user")
