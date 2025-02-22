from datetime import datetime, date
from typing import Any, List, Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base, intpk


USER_ROLE_ID = 1

ADMIN_ROLE_ID = 2


class Role(Base):
    __tablename__ = "role"
    id: Mapped[intpk]
    name: Mapped[str]
    permissions: Mapped[dict[str, Any]]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[float] = mapped_column(default=0.0)
    role: Mapped[Role] = relationship("Role", lazy="selectin")

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
    price: Mapped[float]
    company: Mapped["Company"] = relationship("Company", back_populates="assets", lazy="selectin")


class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    purchase_date: Mapped[date]
    target_sell_date: Mapped[date]
    sell_date: Mapped[date] = mapped_column(nullable=True)
    amount: Mapped[float]

    user: Mapped["User"] = relationship("User", back_populates="transactions", lazy="selectin")
    asset: Mapped["Asset"] = relationship("Asset")
