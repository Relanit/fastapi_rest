from datetime import datetime
from typing import AsyncGenerator, Annotated, Any

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, text, JSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from config import config


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


intpk = Annotated[int, mapped_column(primary_key=True)]


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str]
    permissions: Mapped[dict[str, Any]]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    # role: Mapped[Role] = relationship(back_populates="user")


engine = create_async_engine(f"postgresql+asyncpg://{config.DB_URL}")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
