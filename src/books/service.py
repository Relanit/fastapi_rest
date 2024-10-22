from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from authors.exceptions import AuthorNotFound
from books.exceptions import BookNotFound
from books.schemas import BookUpdate, BookCreate, BookPatchUpdate
from books.models import Book, Author
from database import get_async_session


class BookService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def valid_author_id(self, author_id: int) -> Author:
        result = await self.session.execute(select(Author).where(Author.id == author_id))
        author = result.scalar_one_or_none()
        if not author:
            raise AuthorNotFound()

        return author

    async def create(self, book: BookCreate):
        await self.valid_author_id(book.author_id)

        stmt = insert(Book).values(**book.model_dump()).returning(Book)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, author_id: int | None):
        query = select(Book).limit(limit).offset(skip)
        if author_id is not None:
            await self.valid_author_id(author_id)
            query = query.where(Book.author_id == author_id)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, book_id: int):
        query = select(Book).where(Book.id == book_id)
        result = await self.session.execute(query)
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFound()
        return book

    async def update_full(self, book: Book, updated_book: BookUpdate):
        for key, value in updated_book.model_dump(exclude_unset=True).items():
            setattr(book, key, value)

        merged_book = await self.session.merge(book)
        await self.session.commit()
        return merged_book

    async def update_partial(self, book: Book, book_data: BookPatchUpdate) -> Book:
        update_data = book_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)

        self.session.add(book)
        await self.session.commit()
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()
