from typing import Annotated

from fastapi import Depends

from transactions.exceptions import TransactionNotFound
from transactions.service import TransactionService
from models import Transaction

TransactionServiceDep = Annotated[TransactionService, Depends(TransactionService)]


async def valid_transaction_id(transaction_id: int, service: TransactionServiceDep) -> Transaction:
    transaction = await service.get_by_id(transaction_id)
    if not transaction:
        raise TransactionNotFound()
    return transaction
