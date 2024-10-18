from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field


class Paginator(BaseModel):
    limit: int = Field(10, ge=1, le=100, description="Limit of items to return")
    skip: int = Field(0, ge=0, description="Number of items to skip")


PaginatorDep = Annotated[Paginator, Depends(Paginator)]
