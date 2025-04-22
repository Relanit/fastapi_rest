from decimal import Decimal
from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from assets.exceptions import AssetNotFound
from transactions.exceptions import (
    UserNotFound,
    AssetNotAvailable,
    TransactionNotFound,
    InsufficientFunds,
    InsufficientAssets,
)
from transactions.schemas import TransactionUpdate, TransactionPatchUpdate
from database.database import get_async_session
from database.models import User, Asset, Transaction, UserAsset, TransactionType


class TransactionService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def valid_user_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        if user := result.scalar_one_or_none():
            return user
        raise UserNotFound()

    async def valid_asset_id(self, asset_id: int) -> Asset:
        result = await self.session.execute(select(Asset).where(Asset.id == asset_id))
        if asset := result.scalar_one_or_none():
            return asset
        raise AssetNotFound()

    async def create_buy(self, asset: Asset, amount: Decimal, user: User) -> Transaction:
        if asset.available_count <= 0:
            raise AssetNotAvailable()

        total_value = amount * asset.price

        if user.balance < total_value:
            raise InsufficientFunds()

        user.balance -= total_value
        asset.available_count -= amount

        stmt = select(UserAsset).filter(UserAsset.user_id == user.id, UserAsset.asset_id == asset.id)
        user_asset = await self.session.scalar(stmt)

        if user_asset:
            user_asset.amount += amount
        else:
            stmt = insert(UserAsset).values(user_id=user.id, asset_id=asset.id, amount=amount)
            await self.session.execute(stmt)

        stmt = (
            insert(Transaction)
            .values(
                amount=amount,
                asset_id=asset.id,
                user_id=user.id,
                total_value=total_value,
                type=TransactionType.BUY,
            )
            .returning(Transaction)
        )
        result = await self.session.execute(stmt)
        await self.session.merge(user)
        self.session.add(asset)
        await self.session.commit()
        return result.scalar_one()

    async def create_sell(self, asset: Asset, amount: Decimal, user: User):
        stmt = select(UserAsset).filter(UserAsset.user_id == user.id, UserAsset.asset_id == asset.id)
        user_asset = await self.session.scalar(stmt)
        if not user_asset or user_asset.amount < amount:
            raise InsufficientAssets()

        total_value = amount * asset.price
        user.balance += total_value
        asset.available_count += amount

        if amount == user_asset.amount:
            await self.session.delete(user_asset)
        else:
            user_asset.amount -= amount

        stmt = (
            insert(Transaction)
            .values(
                amount=amount,
                asset_id=asset.id,
                user_id=user.id,
                total_value=total_value,
                type=TransactionType.SELL,
            )
            .returning(Transaction)
        )
        result = await self.session.execute(stmt)
        await self.session.merge(user)
        self.session.add(asset)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, limit: int, skip: int) -> Sequence[Transaction]:
        query = select(Transaction).limit(limit).offset(skip)
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
