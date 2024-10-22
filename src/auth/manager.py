from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelperProtocol
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from models import User
from auth.utils import get_user_db
from database import get_async_session


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = config.SECRET
    verification_token_secret = config.SECRET

    def __init__(
        self,
        user_db: BaseUserDatabase[models.UP, models.ID],
        session: AsyncSession,
        password_helper: Optional[PasswordHelperProtocol] = None,
    ):
        super().__init__(user_db, password_helper)
        self.session = session

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        if user.id == 1:
            stmt = update(User).where(User.id == 1).values(role_id=2, is_superuser=True)
            await self.session.execute(stmt)
            await self.session.commit()
            print("Added admin")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.create_update_dict() if safe else user_create.create_update_dict_superuser()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db), session=Depends(get_async_session)):
    yield UserManager(user_db, session)
