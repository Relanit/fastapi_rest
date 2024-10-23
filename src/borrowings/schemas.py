from datetime import date, timedelta

from pydantic import BaseModel, field_validator


class BorrowBase(BaseModel):
    user_id: int
    book_id: int
    borrow_date: date | None = date.today()
    return_deadline: date | None = date.today() + timedelta(days=30)

    @field_validator("user_id")
    def validate_user_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("User id must be a non-negative number")
        return value

    @field_validator("book_id")
    def validate_book_id(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Book id must be a non-negative number")
        return value

    @field_validator("borrow_date")
    def validate_borrow_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Borrowing date must not be in the future")
        return value

    @field_validator("return_deadline")
    def validate_return_deadline(cls, value: date) -> date:
        if value <= date.today():
            raise ValueError("Return deadline must be in the future.")
        return value


class BorrowCreate(BorrowBase):
    pass


class BorrowUpdate(BorrowBase):
    pass


class BorrowPatchUpdate(BorrowBase):
    user_id: int | None = None
    book_id: int | None = None
    borrow_date: date | None = None
    return_deadline: date | None = None


class BorrowResponse(BorrowBase):
    id: int
    borrow_date: date
    return_deadline: date
    return_date: date | None
