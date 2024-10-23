from datetime import date
from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from books.exceptions import BookNotFound
from borrows.exceptions import UserNotFound, BookNotAvailable
from borrows.schemas import BorrowCreate
from database import get_async_session
from models import Borrow, User, Book


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

    async def valid_book(self, book_id: int) -> Book:
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFound()

        if not book.available_count:
            raise BookNotAvailable()

        return book

    async def create(self, borrow: BorrowCreate) -> Borrow:
        await self.valid_user_id(borrow.user_id)
        book = await self.valid_book(borrow.book_id)

        book.available_count -= 1
        stmt = insert(Borrow).values(**borrow.model_dump() | {"return_date": None}).returning(Borrow)
        result = await self.session.execute(stmt)
        self.session.add(book)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, user_id: int | None) -> Sequence[Borrow]:
        query = select(Borrow).limit(limit).offset(skip)

        if user_id is not None:
            await self.valid_user_id(user_id)
            query = query.where(Borrow.user_id == user_id)

        result = await self.session.execute(query)
        return result.scalars().all()
