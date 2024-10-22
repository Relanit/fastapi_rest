from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from books.dependencies import valid_book_id, BookServiceDep
from books.models import Book
from books.schemas import BookCreate, BookUpdate, BookResponse, BookPatchUpdate
from pagination import PaginatorDep

router = APIRouter(prefix="/books", tags=["Book"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreate,
    service: BookServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    book = await service.create(book)
    return book


@router.get("/", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    pagination_params: PaginatorDep,
    service: BookServiceDep,
    author_id: int | None = None,
):
    books = await service.get_all(pagination_params.limit, pagination_params.skip, author_id)
    return books


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_specific_book(book: Book = Depends(valid_book_id)):
    return book


@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book(
    updated_book: BookUpdate,
    service: BookServiceDep,
    book: Book = Depends(valid_book_id),
    current_user_admin=Depends(current_user_admin),
):
    book = await service.update_full(book, updated_book)
    return book


@router.patch("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def partial_update_book(
    book_data: BookPatchUpdate,
    service: BookServiceDep,
    book: Book = Depends(valid_book_id),
    current_user_admin=Depends(current_user_admin),
):
    updated_book = await service.update_partial(book, book_data)
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    service: BookServiceDep, book: Book = Depends(valid_book_id), current_user_admin=Depends(current_user_admin)
):
    await service.delete(book)
