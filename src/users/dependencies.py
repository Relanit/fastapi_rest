from typing import Annotated

from fastapi import Depends

from users.service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
