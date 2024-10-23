from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin, current_user
from borrowings.exceptions import BorrowingsAccessForbidden
from borrowings.schemas import BorrowResponse, BorrowCreate, BorrowUpdate, BorrowPatchUpdate
from borrowings.dependencies import BorrowServiceDep, valid_borrowing_id
from models import Borrowing, User
from pagination import PaginatorDep

router = APIRouter(prefix="/borrowings", tags=["Borrowing"])


@router.post("/", response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
async def create_borrowing(
    borrowing: BorrowCreate,
    service: BorrowServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    borrowing = await service.create(borrowing)
    return borrowing


@router.get("/", response_model=list[BorrowResponse], status_code=status.HTTP_200_OK)
async def get_borrowings(
    pagination: PaginatorDep,
    service: BorrowServiceDep,
    user_id: int | None = None,
    current_user: User = Depends(current_user),
):
    if user_id is not None and user_id != current_user.id and not current_user.role_id == 2:
        raise BorrowingsAccessForbidden()

    borrowings = await service.get_all(pagination.limit, pagination.skip, user_id)
    return borrowings


@router.get("/{borrowing_id}", response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def get_specific_borrowing(
    borrowing: Borrowing = Depends(valid_borrowing_id), current_user_admin=Depends(current_user_admin)
):
    return borrowing


@router.put("/{borrowing_id}", response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def update_borrowing(
    updated_borrowing: BorrowUpdate,
    service: BorrowServiceDep,
    borrowing: Borrowing = Depends(valid_borrowing_id),
    current_user_admin=Depends(current_user_admin),
):
    borrowing = await service.update_full(borrowing, updated_borrowing)
    return borrowing


@router.patch("/{borrowing_id}", response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def partial_update_borrowing(
    borrowing_data: BorrowPatchUpdate,
    service: BorrowServiceDep,
    borrowing: Borrowing = Depends(valid_borrowing_id),
    current_user_admin=Depends(current_user_admin),
):
    updated_borrowing = await service.update_partial(borrowing, borrowing_data)
    return updated_borrowing


@router.delete("/{borrowing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_borrowing(
    service: BorrowServiceDep,
    borrowing: Borrowing = Depends(valid_borrowing_id),
    current_user_admin=Depends(current_user_admin),
):
    await service.delete(borrowing)
