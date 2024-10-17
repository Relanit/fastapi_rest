from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from books.models import Book
from database import get_async_session
from dependencies import Paginator

router = APIRouter(prefix="/books", tags=["Book"])


@router.get("/")
async def get_books(
    session: AsyncSession = Depends(get_async_session), pagination_params: Paginator = Depends(Paginator)
):
    query = select(Book).limit(pagination_params.limit).offset(pagination_params.skip)
    result = await session.execute(query)
    books = result.scalars().all()

    return {
        "status": "success",
        "data": books,
        "details": {
            "total": len(books),
            "limit": pagination_params.limit,
            "skip": pagination_params.skip,
        },
    }
