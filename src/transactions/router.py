from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin, current_user
from transactions.exceptions import TransactionsAccessForbidden
from transactions.schemas import TransactionResponse, TransactionCreate, TransactionUpdate, TransactionPatchUpdate
from transactions.dependencies import TransactionServiceDep, valid_transaction_id
from database.models import Transaction, User, ADMIN_ROLE_ID
from pagination import PaginatorDep


router = APIRouter(prefix="/transactions", tags=["Transaction"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    service: TransactionServiceDep,
    current_user: User = Depends(current_user),
):
    return await service.create(transaction, current_user)


@router.get("/", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(
    pagination: PaginatorDep,
    service: TransactionServiceDep,
    user_id: int | None = None,
    current_user: User = Depends(current_user),
):
    if (user_id is None or current_user.id != user_id) and current_user.role_id != ADMIN_ROLE_ID:
        raise TransactionsAccessForbidden()

    return await service.get_all(pagination.limit, pagination.skip, user_id)


@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def get_specific_transaction(
    transaction: Transaction = Depends(valid_transaction_id), current_user_admin=Depends(current_user_admin)
):
    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def update_transaction(
    updated_transaction: TransactionUpdate,
    service: TransactionServiceDep,
    transaction: Transaction = Depends(valid_transaction_id),
    current_user_admin=Depends(current_user_admin),
):
    return await service.update_full(transaction, updated_transaction)


@router.patch("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def partial_update_transaction(
    transaction_data: TransactionPatchUpdate,
    service: TransactionServiceDep,
    transaction: Transaction = Depends(valid_transaction_id),
    current_user_admin=Depends(current_user_admin),
):
    return await service.update_partial(transaction, transaction_data)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    service: TransactionServiceDep,
    transaction: Transaction = Depends(valid_transaction_id),
    current_user_admin=Depends(current_user_admin),
):
    await service.delete(transaction)
