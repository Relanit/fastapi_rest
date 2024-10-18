from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from books.exceptions import BookNotFound
from books.schemas import BookUpdate, BookCreate
from books.models import Book
from database import get_async_session


class BookService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, book: BookCreate):
        stmt = insert(Book).values(**book.model_dump()).returning(Book)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int):
        query = select(Book).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, book_id: int):
        query = select(Book).where(Book.id == book_id)
        result = await self.session.execute(query)
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFound()
        return book

    async def update_by_id(self, book_id: int, updated_book: BookUpdate):
        await self.get_by_id(book_id)  # validate book_id

        stmt = update(Book).where(Book.id == book_id).values(**updated_book.model_dump()).returning(Book)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def delete_by_id(self, book_id: int):
        await self.get_by_id(book_id)  # validate book_id

        stmt = delete(Book).where(Book.id == book_id)
        await self.session.execute(stmt)
        await self.session.commit()


BookServiceDep = Annotated[BookService, Depends(BookService)]
