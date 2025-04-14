from decimal import Decimal

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    username: str
    role_id: int
    balance: Decimal


class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int

