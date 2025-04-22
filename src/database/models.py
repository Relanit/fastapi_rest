from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Any, List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from pydantic import EmailStr
from sqlalchemy import text, ForeignKey, String, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from database.database import Base, intpk


USER_ROLE_ID = 1

ADMIN_ROLE_ID = 2


class TransactionType(Enum):
    BUY = "buy"
    SELL = "sell"


class Role(Base):
    __tablename__ = "role"
    id: Mapped[intpk]
    name: Mapped[str]
    permissions: Mapped[dict[str, Any]]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[EmailStr] = mapped_column(String(length=320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=20, scale=10), default=Decimal("0.0")
    )  # Баланс пользователя в USD (долларах США)
    role: Mapped[Role] = relationship("Role", lazy="selectin")

    user_assets: Mapped[List["UserAsset"]] = relationship(
        "UserAsset", back_populates="user", lazy="selectin", cascade="all, delete-orphan"
    )
    transactions = relationship("Transaction", back_populates="user", lazy="selectin")


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    profile: Mapped[Optional[str]] = mapped_column(nullable=True)
    foundation_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="company", lazy="selectin")


class Asset(Base):
    __tablename__ = "asset"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    listed_year: Mapped[int]
    ticker: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    available_count: Mapped[int] = mapped_column(default=0)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=10))  # Цена актива в USD (долларах США)
    company: Mapped["Company"] = relationship("Company", back_populates="assets", lazy="selectin")


class UserAsset(Base):
    __tablename__ = "user_asset"
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=20, scale=10), default=Decimal("0.0")
    )  # Количество актива в собственности пользователя

    user: Mapped["User"] = relationship("User", back_populates="user_assets", lazy="selectin")
    asset: Mapped["Asset"] = relationship("Asset", lazy="selectin")

    __table_args__ = (
        UniqueConstraint(
            "user_id", "asset_id", name="unique_user_asset"
        ),  # Чтобы не было дубликатов для одного пользователя и актива
    )


class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    type: Mapped[TransactionType] = mapped_column(SQLAlchemyEnum(TransactionType))
    transaction_datetime: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(precision=20, scale=10))  # Количество актива
    total_value: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=20, scale=10)
    )  # Сумма транзакции в USD (долларах США)

    user: Mapped["User"] = relationship("User", back_populates="transactions", lazy="selectin")
    asset: Mapped["Asset"] = relationship("Asset")
