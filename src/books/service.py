from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select, or_, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from authors.exceptions import AuthorNotFound
from books.exceptions import BookNotFound
from books.schemas import BookUpdate, BookCreate, BookPatchUpdate
from models import Book, Author
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

    async def create(self, book: BookCreate) -> Book:
        await self.valid_author_id(book.author_id)

        stmt = insert(Book).values(**book.model_dump()).returning(Book)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, author_id: int | None) -> Sequence[Book]:
        if author_id is not None:
            author = await self.valid_author_id(author_id)
            return author.books[skip : skip + limit]

        query = select(Book).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, book_id: int) -> Book:
        query = select(Book).where(Book.id == book_id)
        result = await self.session.execute(query)
        book = result.scalar_one_or_none()
        return book

    async def search_books(self, search_query: str) -> Sequence[Book]:
        search_terms = search_query.split()

        title_conditions = [Book.title.ilike(f"%{term}%") for term in search_terms]
        author_conditions = [Author.name.ilike(f"%{term}%") for term in search_terms]

        book_cases = [(Book.title.ilike(f"%{term}%"), 1) for term in search_terms]
        author_cases = [(Author.name.ilike(f"%{term}%"), 1) for term in search_terms]

        title_match_score = case(*book_cases, else_=0)
        author_match_score = case(*author_cases, else_=0)

        query = (
            select(Book)
            .join(Author)
            .filter(or_(*title_conditions, *author_conditions))
            .order_by(func.coalesce(title_match_score, 0) + func.coalesce(author_match_score, 0).desc())
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_full(self, book: Book, updated_book: BookUpdate) -> Book:
        await self.valid_author_id(book.author_id)

        for key, value in updated_book.model_dump(exclude_unset=True).items():
            setattr(book, key, value)

        merged_book = await self.session.merge(book)
        await self.session.commit()
        return merged_book

    async def update_partial(self, book: Book, book_data: BookPatchUpdate) -> Book:
        update_data = book_data.model_dump(exclude_unset=True)

        if "author_id" in update_data:
            await self.valid_author_id(update_data["author_id"])

        for key, value in update_data.items():
            setattr(book, key, value)

        self.session.add(book)
        await self.session.commit()
        return book

    async def delete(self, book: Book) -> None:
        await self.session.delete(book)
        await self.session.commit()
