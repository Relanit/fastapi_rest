from datetime import date

from pydantic import BaseModel, field_validator


class BookBase(BaseModel):
    title: str
    published_year: int | None = None
    isbn: str | None = None
    description: str | None = None
    available_count: int

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not (1 < len(value) < 100):
            raise ValueError("Book title must be at least 1 character long.")
        return value

    @field_validator("published_year")
    def validate_published_year(cls, value: int | None) -> int | None:
        if value is not None:
            current_year = date.today().year
            if value > current_year:
                raise ValueError("Published year cannot be in the future.")
        return value

    @field_validator("available_count")
    def validate_available_count(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Available count must be a non-negative number.")
        return value


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    pass


class BookPatchUpdate(BookBase):
    title: str | None = None
    available_count: int | None = None


class BookResponse(BookBase):
    id: int
    author_id: int
