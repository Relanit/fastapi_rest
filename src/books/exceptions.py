from fastapi import HTTPException


class BookAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail={"status": "error", "data": None, "details": "Book already exists"})


class BookNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={"status": "error", "data": None, "details": "Book not found"})
