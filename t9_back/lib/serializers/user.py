import typing as t

from pydantic import BaseModel, EmailStr

from ..utils import security


class UserIn(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    class Config:
        orm_mode = True
        fields = {
            "salt": {"exclude": True},
            "hashed_password": {"exclude": True},
        }

    email: str
    salt: str
    hashed_password: str
    token: t.Optional[str]

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def make_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)
