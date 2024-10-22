from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from authors.dependencies import valid_author_id, AuthorServiceDep
from authors.schemas import AuthorCreate, AuthorUpdate, AuthorResponse, AuthorPatchUpdate
from models import Author
from pagination import PaginatorDep

router = APIRouter(prefix="/authors", tags=["Author"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
    author: AuthorCreate,
    service: AuthorServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    author = await service.create(author)
    return author


@router.get("/", response_model=list[AuthorResponse], status_code=status.HTTP_200_OK)
async def get_authors(pagination_params: PaginatorDep, service: AuthorServiceDep):
    authors = await service.get_all(pagination_params.limit, pagination_params.skip)
    return authors


@router.get("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def get_specific_author(author: Author = Depends(valid_author_id)):
    return author


@router.put("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def update_author(
    updated_author: AuthorUpdate,
    service: AuthorServiceDep,
    author: Author = Depends(valid_author_id),
    current_user_admin=Depends(current_user_admin),
):
    author_updated = await service.update_full(author, updated_author)
    return author_updated


@router.patch("/{author_id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def partial_update_author(
    author_data: AuthorPatchUpdate,
    service: AuthorServiceDep,
    author: Author = Depends(valid_author_id),
    current_user_admin=Depends(current_user_admin),
):
    updated_author = await service.update_partial(author, author_data)
    return updated_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    service: AuthorServiceDep, author: Author = Depends(valid_author_id), current_user_admin=Depends(current_user_admin)
):
    await service.delete(author)
