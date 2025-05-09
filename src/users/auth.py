from fastapi import Depends, HTTPException
from fastapi import status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from .manager import get_user_manager
from database.models import User, ADMIN_ROLE_ID
from config import config

cookie_transport = CookieTransport(cookie_name="library", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


async def current_user_admin(user: User = Depends(current_user)):
    if user.role_id != ADMIN_ROLE_ID and user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin role is required for this endpoint"
        )

    return user
