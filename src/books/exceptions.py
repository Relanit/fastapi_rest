from fastapi import HTTPException


class BookNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail={"status": "error", "data": None, "details": "Book not found"})
