import typing as t
from datetime import datetime

from pydantic import BaseModel


class Hit(BaseModel):
    created_at: datetime
    ip: str
    user_agent: str


class Stat(BaseModel):
    class Config:
        orm_mode = True

    hits: int
    updated_at: datetime
    hit_count: t.List[Hit]


class LinkIn(BaseModel):
    original_url: str


class Link(BaseModel):
    class Config:
        orm_mode = True

    original_url: str
    short_url: str
    qr: t.Optional[str]
    stat: Stat


class LinkTest(BaseModel):
    class Config:
        orm_mode = True

    original_url: str
    short_url: str
    qr: t.Optional[str]
    stat: Stat
