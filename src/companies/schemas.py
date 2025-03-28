from datetime import date

from pydantic import BaseModel, constr, Field


class CompanyBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=100)
    profile: str | None = None
    foundation_date: date | None = Field(None, le=date.today())


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyPatchUpdate(CompanyBase):
    name: str | None = None
    profile: str | None = None
    foundation_date: date | None = None


class CompanyResponse(CompanyBase):
    id: int
