from typing import AsyncGenerator, Annotated, Any

from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from config import config


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


intpk = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]


url = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
engine = create_async_engine(url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


