from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from authors.exceptions import AuthorAlreadyExists
from authors.schemas import AuthorUpdate, AuthorCreate, AuthorPatchUpdate
from models import Author
from database import get_async_session


class AuthorService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create(self, author: AuthorCreate) -> Author:
        author.name = author.name.title()
        existing_author = await self.get_by_name(author.name)
        if existing_author:
            raise AuthorAlreadyExists()

        stmt = insert(Author).values(**author.model_dump()).returning(Author)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int) -> Sequence[Author]:
        query = select(Author).limit(limit).offset(skip)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, author_id: int) -> Author | None:
        query = select(Author).where(Author.id == author_id)
        result = await self.session.execute(query)
        author = result.scalar_one_or_none()
        return author

    async def get_by_name(self, name: str) -> Author | None:
        query = select(Author).where(Author.name == name)
        result = await self.session.execute(query)
        author = result.scalar_one_or_none()
        return author

    async def update_full(self, author: Author, updated_author: AuthorUpdate) -> Author:
        for key, value in updated_author.model_dump(exclude_unset=True).items():
            setattr(author, key, value)

        merged_author = await self.session.merge(author)
        await self.session.commit()
        return merged_author

    async def update_partial(self, author: Author, update_data: AuthorPatchUpdate) -> Author:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)

        self.session.add(author)
        await self.session.commit()
        return author

    async def delete(self, author: Author) -> None:
        await self.session.delete(author)
        await self.session.commit()
