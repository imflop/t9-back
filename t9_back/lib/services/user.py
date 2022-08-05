import dataclasses as dc

from ..dal.users import UserRepository
from ..serializers.user import User, UserIn


@dc.dataclass(repr=False)
class UserService:
    user_repository: UserRepository

    async def is_email_taken(self, user_email: str) -> bool:
        return await self.user_repository.is_email_taken(user_email)

    async def get_user(self, user_email: str) -> User:
        user_model = await self.user_repository.get_user(user_email)

        return User.from_orm(user_model)

    async def create_user(self, new_user: UserIn) -> User:
        user = User(email=new_user.email, salt="", hashed_password="")
        user.make_password(new_user.password)
        await self.user_repository.create_user(user.email, user.salt, user.hashed_password)

        return user
