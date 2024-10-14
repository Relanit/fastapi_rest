from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.authors.schemas import OperationCreate
from src.authors.models import Author
from src.database import get_async_session

router = APIRouter(prefix="/authors", tags=["Author"])


@router.get("/")
async def get_specific_authors(name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Author).where(Author.name == name)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/")
async def add_specific_author(new_author: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Author).values(**new_author.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
