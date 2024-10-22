from datetime import date, datetime

from pydantic import BaseModel, field_validator


class AuthorBase(BaseModel):
    name: str
    biography: str | None = None
    date_of_birth: date | None = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not (1 < len(value) < 100):
            raise ValueError("Author name must be between 2 and 100 characters long.")
        return value.title()

    @field_validator("date_of_birth", mode="before")
    def validate_date_of_birth(cls, value: str | date) -> date:
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")

        if value > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return value


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorPatchUpdate(AuthorBase):
    name: str | None = None


class AuthorResponse(AuthorBase):
    id: int
