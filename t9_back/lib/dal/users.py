import dataclasses as dc
import typing as t

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..errors import EntityDoesNotExist
from .models.users import UserModel


UserFilter = t.Union[str, int, UserModel]


@dc.dataclass(repr=False)
class UserRepository:
    db: AsyncSession

    async def is_email_taken(self, user_email: str) -> bool:
        q = select(UserModel).where(UserModel.email == user_email)
        result = await self.db.execute(q)
        row = result.fetchone()
        return bool(row)

    async def _get_by_id(self, id: int) -> UserModel:
        q = select(UserModel).where(UserModel.id == id)
        result = await self.db.execute(q)

        try:
            row = result.one()
        except NoResultFound as err:
            raise EntityDoesNotExist(f"Entity by {id} not found") from err

        return row[UserModel]

    async def _get_by_email(self, email: str) -> UserModel:
        q = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(q)

        try:
            row = result.one()
        except NoResultFound as err:
            raise EntityDoesNotExist(f"Entity by {email} not found") from err

        return row[UserModel]

    async def get_user(self, user_filter: UserFilter) -> UserModel:
        if isinstance(user_filter, int):
            return await self._get_by_id(user_filter)
        elif isinstance(user_filter, str):
            return await self._get_by_email(user_filter)
        elif isinstance(user_filter, UserModel):
            return user_filter
        else:
            raise EntityDoesNotExist(f"Entity: {user_filter} not found")

    async def _store_model(self, user: UserModel) -> UserModel:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_user(self, email: str, salt: str, password: str) -> UserModel:
        user_model = UserModel(email=email, salt=salt, password=password)
        self.db.add(user_model)
        return await self._store_model(user_model)
