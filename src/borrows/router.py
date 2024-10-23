from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from borrows.schemas import BorrowResponse, BorrowCreate
from borrows.dependencies import BorrowServiceDep
from pagination import PaginatorDep

router = APIRouter(prefix="/borrows", tags=["Borrow"])


@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow(
    borrow: BorrowCreate,
    service: BorrowServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    book = await service.create(borrow)
    return book


@router.get("/", response_model=list[BorrowResponse], status_code=status.HTTP_200_OK)
async def get_borrows(
    pagination: PaginatorDep,
    service: BorrowServiceDep,
    user_id: int | None = None,
    current_user_admin=Depends(current_user_admin),
):
    book = await service.get_all(pagination.limit, pagination.skip, user_id)
    return book
