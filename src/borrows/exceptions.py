from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "data": None, "details": "User not found"}
        )


class BookNotAvailable(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "error", "data": None, "details": "Book not available"},
        )
