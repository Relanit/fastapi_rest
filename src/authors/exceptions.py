from fastapi import HTTPException


class AuthorAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail={"status": "error", "data": None, "details": "Author already exists"})


class AuthorNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={"status": "error", "data": None, "details": "Author not found"})


