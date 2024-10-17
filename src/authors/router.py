from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import current_user_admin
from authors.schemas import OperationCreate
from books.models import Author
from database import get_async_session
from dependencies import Paginator

router = APIRouter(prefix="/authors", tags=["Author"])


@router.get("/")
async def get_authors(
    session: AsyncSession = Depends(get_async_session), pagination_params: Paginator = Depends(Paginator)
):
    query = select(Author).limit(pagination_params.limit).offset(pagination_params.skip)
    result = await session.execute(query)
    authors = result.scalars().all()

    return {
        "status": "success",
        "data": authors,
        "details": {
            "total": len(authors),
            "limit": pagination_params.limit,
            "skip": pagination_params.skip,
        },
    }


@router.get("/{author_id}")
async def get_specific_author(author_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Author).where(Author.id == author_id)
    result = await session.execute(query)
    return {"status": "success", "data": result.mappings().all(), "details": None}


@router.post("/")
async def create_author(
    new_author: OperationCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user_admin=Depends(current_user_admin),
):
    stmt = insert(Author).values(**new_author.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
