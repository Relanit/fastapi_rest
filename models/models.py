from datetime import datetime
from typing import Annotated, Any

from dataclasses import dataclass
from sqlalchemy import text, JSON, ForeignKey, String, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


intpk = Annotated[int, mapped_column(primary_key=True)]


@dataclass
class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str]
    permissions: Mapped[dict[str, Any]]


@dataclass
class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    role: Mapped[Role] = relationship(back_populates="user")
