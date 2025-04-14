from datetime import date

from pydantic import BaseModel, constr, field_validator


class CompanyBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=2, max_length=100)
    profile: str | None = None
    foundation_date: date | None = None

    @field_validator("foundation_date")
    def check_foundation_date(cls, value: date | None) -> date | None:
        if value is not None and value > date.today():
            raise ValueError("foundation_date не может быть в будущем")
        return value


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
