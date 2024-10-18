from fastapi import HTTPException


class AuthorNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={"status": "error", "data": None, "details": "Author not found"})
