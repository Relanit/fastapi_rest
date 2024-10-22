from typing import Annotated

from fastapi import Depends

from authors.exceptions import AuthorNotFound
from authors.service import AuthorService
from models import Author

AuthorServiceDep = Annotated[AuthorService, Depends(AuthorService)]


async def valid_author_id(author_id: int, service: AuthorServiceDep) -> Author:
    author = await service.get_by_id(author_id)
    if not author:
        raise AuthorNotFound()
    return author
