from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from authors.schemas import OperationCreate, OperationUpdate, AuthorResponse
from authors.service import AuthorServiceDep
from pagination import PaginatorDep

router = APIRouter(prefix="/authors", tags=["Author"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: OperationCreate, service: AuthorServiceDep, current_user_admin=Depends(current_user_admin)
):
    author = await service.create(author)
    return author


@router.get("/", response_model=list[AuthorResponse], status_code=status.HTTP_200_OK)
async def get_authors(pagination_params: PaginatorDep, service: AuthorServiceDep):
    authors = await service.get_all(pagination_params.limit, pagination_params.skip)
    return authors


@router.get("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def get_specific_author(author_id: int, service: AuthorServiceDep):
    author = await service.get_by_id(author_id)
    return author


@router.put("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def update_author(
    author_id: int,
    updated_author: OperationUpdate,
    service: AuthorServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    author = await service.update_by_id(author_id, updated_author)
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, service: AuthorServiceDep, current_user_admin=Depends(current_user_admin)):
    await service.delete_by_id(author_id)
