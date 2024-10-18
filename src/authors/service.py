from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from authors.exceptions import AuthorNotFound
from authors.schemas import OperationUpdate, OperationCreate
from books.models import Author
from database import get_async_session


class AuthorService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, new_author: OperationCreate):
        stmt = insert(Author).values(**new_author.model_dump()).returning(Author)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int):
        query = select(Author).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, author_id: int):
        query = select(Author).where(Author.id == author_id)
        result = await self.session.execute(query)
        author = result.scalar_one_or_none()
        if not author:
            raise AuthorNotFound()
        return author

    async def update_by_id(self, author_id: int, updated_author: OperationUpdate):
        await self.get_by_id(author_id)  # validate author_id

        stmt = update(Author).where(Author.id == author_id).values(**updated_author.model_dump()).returning(Author)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def delete_by_id(self, author_id: int):
        await self.get_by_id(author_id)  # validate author_id

        stmt = delete(Author).where(Author.id == author_id)
        await self.session.execute(stmt)
        await self.session.commit()


AuthorServiceDep = Annotated[AuthorService, Depends(AuthorService)]
