from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    name: str
    biography: str
    date_of_birth: datetime