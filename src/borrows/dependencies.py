from typing import Annotated

from fastapi import Depends

from borrows.service import BorrowService

BorrowServiceDep = Annotated[BorrowService, Depends(BorrowService)]



