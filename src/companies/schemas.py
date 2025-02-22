from datetime import date, datetime

from pydantic import BaseModel, field_validator


class CompanyBase(BaseModel):
    name: str
    profile: str | None = None
    foundation_date: date | None = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Название компании должно содержать от 2 до 100 символов.")
        value = value.strip()
        if not (2 <= len(value) <= 100):
            raise ValueError("Название компании должно содержать от 2 до 100 символов.")
        return value.title()

    @field_validator("foundation_date", mode="before")
    def validate_foundation_date(cls, value: str | date) -> date | None:
        if not value:
            return value
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError("Неверный формат даты. Используйте 'YYYY-MM-DD'.") from e
        if value > date.today():
            raise ValueError("Дата основания не может быть в будущем.")
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
