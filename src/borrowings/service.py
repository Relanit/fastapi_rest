from datetime import date
from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from books.exceptions import BookNotFound
from borrowings.exceptions import UserNotFound, BookNotAvailable, BorrowingNotFound
from borrowings.schemas import BorrowCreate, BorrowUpdate, BorrowPatchUpdate
from database import get_async_session
from models import Borrowing, User, Book


class BorrowService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def valid_user_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound()
        return user

    async def valid_book_id(self, book_id: int) -> Book:
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFound()

        return book

    async def create(self, borrowing: BorrowCreate) -> Borrowing:
        await self.valid_user_id(borrowing.user_id)
        book = await self.valid_book_id(borrowing.book_id)
        if not book.available_count:
            raise BookNotAvailable()

        book.available_count -= 1
        stmt = insert(Borrowing).values(**borrowing.model_dump() | {"return_date": None}).returning(Borrowing)
        result = await self.session.execute(stmt)
        self.session.add(book)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, user_id: int | None) -> Sequence[Borrowing]:
        query = select(Borrowing).limit(limit).offset(skip)

        if user_id is not None:
            await self.valid_user_id(user_id)
            query = query.where(Borrowing.user_id == user_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, borrowing_id: int):
        query = select(Borrowing).where(Borrowing.id == borrowing_id)
        result = await self.session.execute(query)
        book = result.scalar_one_or_none()
        return book

    async def update_full(self, borrowing: Borrowing, updated_borrowing: BorrowUpdate) -> Borrowing:
        await self.valid_user_id(borrowing.user_id)
        await self.valid_book_id(borrowing.user_id)

        for key, value in updated_borrowing.model_dump(exclude_unset=True).items():
            setattr(borrowing, key, value)

        merged_book = await self.session.merge(borrowing)
        await self.session.commit()
        return merged_book

    async def update_partial(self, borrowing: Borrowing, borrowing_data: BorrowPatchUpdate) -> Borrowing:
        update_data = borrowing_data.model_dump(exclude_unset=True)

        if "user_id" in update_data:
            await self.valid_user_id(update_data["user_id"])
        if "book_id" in update_data:
            await self.valid_book_id(update_data["book_id"])

        for key, value in update_data.items():
            setattr(borrowing, key, value)

        self.session.add(borrowing)
        await self.session.commit()
        return borrowing

    async def delete(self, borrowing: Borrowing) -> None:
        await self.session.delete(borrowing)
        await self.session.commit()
