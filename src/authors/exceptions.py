from fastapi import HTTPException, status


class AuthorAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "data": None, "details": "Author already exists"},
        )


class AuthorNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "data": None, "details": "Author not found"},
        )
