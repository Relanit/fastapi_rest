from typing import Annotated

from fastapi import Depends

from borrowings.exceptions import BorrowingNotFound
from borrowings.service import BorrowService
from models import Borrowing

BorrowServiceDep = Annotated[BorrowService, Depends(BorrowService)]


async def valid_borrowing_id(borrowing_id: int, service: BorrowServiceDep) -> Borrowing:
    borrowing = await service.get_by_id(borrowing_id)
    if not borrowing:
        raise BorrowingNotFound()
    return borrowing
