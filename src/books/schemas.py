from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author_id: int
    published_year: int | None
    isbn: int | None
    description: str | None
    available_count: int


class BookUpdate(BaseModel):
    title: str
    author_id: int
    published_year: int | None
    isbn: str | None
    description: str | None
    available_count: int


class BookResponse(BaseModel):
    id: int
    title: str
    author_id: int
    published_year: int | None
    isbn: str | None
    description: str | None
    available_count: int
