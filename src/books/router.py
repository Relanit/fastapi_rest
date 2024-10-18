from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import current_user_admin
from books.models import Book
from books.schemas import BookCreate, BookUpdate
from database import get_async_session
from pagination import Paginator

router = APIRouter(prefix="/books", tags=["Book"])


@router.post("/")
async def create_book(
    new_book: BookCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user_admin=Depends(current_user_admin),
):
    stmt = insert(Book).values(**new_book.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


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


@router.get("/{book_id}")
async def get_specific_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Book).where(Book.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail={"status": "error", "data": None, "details": "Book not found"})

    return {"status": "success", "data": book, "details": None}


@router.put("/{book_id}")
async def update_book(
    book_id: int,
    updated_book: BookUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user_admin=Depends(current_user_admin),
):
    query = select(Book).where(Book.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    stmt = update(Book).where(Book.id == book_id).values(**updated_book.model_dump())
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}


@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user_admin=Depends(current_user_admin),
):
    query = select(Book).where(Book.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    stmt = delete(Book).where(Book.id == book_id)
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}
