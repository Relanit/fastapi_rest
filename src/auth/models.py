from datetime import datetime
from typing import Any

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base, intpk


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

    role: Mapped[Role] = relationship("Role", lazy='selectin')
