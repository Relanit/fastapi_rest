from typing import Annotated

from fastapi import Depends

from books.exceptions import BookNotFound
from models import Author, Book
from books.service import BookService

BookServiceDep = Annotated[BookService, Depends(BookService)]


async def valid_book_id(book_id: int, service: BookServiceDep) -> Book:
    book = await service.get_by_id(book_id)
    if not book:
        raise BookNotFound()
    return book
