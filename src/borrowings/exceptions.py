from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "data": None, "details": "User not found"}
        )


class BorrowingNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "data": None, "details": "Borrowing not found"},
        )


class BookNotAvailable(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "error", "data": None, "details": "Book not available"},
        )


class BorrowingsAccessForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"status": "error", "data": None, "details": "Access to the user's borrowed books is forbidden"},
        )
