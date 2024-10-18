from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    name: str
    biography: str
    date_of_birth: datetime


class OperationUpdate(BaseModel):
    name: str
    biography: str
    date_of_birth: datetime


class AuthorResponse(BaseModel):
    id: int
    name: str
    biography: str | None
    date_of_birth: datetime | None
