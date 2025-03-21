import math
from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from assets.exceptions import AssetNotFound
from transactions.exceptions import UserNotFound, AssetNotAvailable, TransactionNotFound, InsufficientFunds, \
    UserMismatch, TransactionAmountMismatch
from transactions.schemas import TransactionCreate, TransactionUpdate, TransactionPatchUpdate
from database.database import get_async_session
from database.models import User, Asset, Transaction


class TransactionService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def valid_user_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFound()
        return user

    async def valid_asset_id(self, asset_id: int) -> Asset:
        result = await self.session.execute(select(Asset).where(Asset.id == asset_id))
        asset = result.scalar_one_or_none()
        if not asset:
            raise AssetNotFound()
        return asset

    async def create(self, transaction: TransactionCreate, user: User) -> Transaction:
        if transaction.user_id != user.id:
            raise UserMismatch()

        asset = await self.valid_asset_id(transaction.asset_id)
        if asset.available_count <= 0:
            raise AssetNotAvailable()

        if not math.isclose(transaction.amount, asset.price, rel_tol=1e-9, abs_tol=1e-2):
            raise TransactionAmountMismatch()

        if user.balance < asset.price:
            raise InsufficientFunds()

        user.balance -= asset.price
        asset.available_count -= 1

        stmt = insert(Transaction).values(**transaction.model_dump(), sell_date=None).returning(Transaction)
        result = await self.session.execute(stmt)
        await self.session.merge(user)
        self.session.add(asset)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int, user_id: int | None) -> Sequence[Transaction]:
        query = select(Transaction).limit(limit).offset(skip)
        if user_id is not None:
            await self.valid_user_id(user_id)
            query = query.where(Transaction.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> Transaction:
        query = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.session.execute(query)
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise TransactionNotFound()
        return transaction

    async def update_full(self, transaction: Transaction, updated_transaction: TransactionUpdate) -> Transaction:
        await self.valid_user_id(transaction.user_id)
        await self.valid_asset_id(transaction.asset_id)
        for key, value in updated_transaction.model_dump(exclude_unset=True).items():
            setattr(transaction, key, value)
        merged_transaction = await self.session.merge(transaction)
        await self.session.commit()
        return merged_transaction

    async def update_partial(self, transaction: Transaction, transaction_data: TransactionPatchUpdate) -> Transaction:
        update_data = transaction_data.model_dump(exclude_unset=True)
        if "user_id" in update_data:
            await self.valid_user_id(update_data["user_id"])
        if "asset_id" in update_data:
            await self.valid_asset_id(update_data["asset_id"])
        for key, value in update_data.items():
            setattr(transaction, key, value)
        self.session.add(transaction)
        await self.session.commit()
        return transaction

    async def delete(self, transaction: Transaction) -> None:
        await self.session.delete(transaction)
        await self.session.commit()
