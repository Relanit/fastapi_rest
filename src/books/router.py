from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from books.schemas import BookCreate, BookUpdate, BookResponse
from books.service import BookServiceDep
from pagination import PaginatorDep

router = APIRouter(prefix="/books", tags=["Book"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, service: BookServiceDep, current_user_admin=Depends(current_user_admin)):
    book = await service.create(book)
    return book


@router.get("/", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(pagination_params: PaginatorDep, service: BookServiceDep):
    books = await service.get_all(pagination_params.limit, pagination_params.skip)
    return books


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_specific_book(book_id: int, service: BookServiceDep):
    book = await service.get_by_id(book_id)
    return book


@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book(
    book_id: int,
    updated_book: BookUpdate,
    service: BookServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    book = await service.update_by_id(book_id, updated_book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, service: BookServiceDep, current_user_admin=Depends(current_user_admin)):
    await service.delete_by_id(book_id)
