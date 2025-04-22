from fastapi import APIRouter, Depends
from fastapi import status

from users.auth import current_user_admin
from transactions.schemas import TransactionResponse, TransactionUpdate, TransactionPatchUpdate
from transactions.dependencies import TransactionServiceDep, valid_transaction_id
from database.models import Transaction, User
from pagination import PaginatorDep


router = APIRouter(prefix="/transactions", tags=["Transaction"])


@router.get("/", response_model=list[TransactionResponse], status_code=status.HTTP_200_OK)
async def get_transactions(
    pagination: PaginatorDep,
    service: TransactionServiceDep,
    current_user_admin: User = Depends(current_user_admin),
):
    return await service.get_all(pagination.limit, pagination.skip)


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
