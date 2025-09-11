from typing import AsyncGenerator, Annotated, Any, Optional

from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from config import config
from logger import logger


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


intpk = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]

_engine: Optional[AsyncEngine] = None
_async_session_maker: Optional[async_sessionmaker] = None


def setup_database():
    global _engine, _async_session_maker

    if _engine is not None:
        return

    url = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    _engine = create_async_engine(url)
    _async_session_maker = async_sessionmaker(_engine, expire_on_commit=False)
    logger.info("Database engine and session maker have been initialized.")


async def dispose_database_engine():
    global _engine, _async_session_maker
    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None
        logger.info("Database engine and session maker have been disposed.")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if _async_session_maker is None:
        raise RuntimeError("Database session factory is not initialized. Call setup_database() on application startup.")

    async with _async_session_maker() as session:
        yield session
