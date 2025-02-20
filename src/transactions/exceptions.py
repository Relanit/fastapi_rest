from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "data": None, "details": "User not found"}
        )


class UserMismatch(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "data": None, "details": "User id mismatched with current user"},
        )


class TransactionAmountMismatch(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "data": None, "details": "Transaction amount mismatched with asset price"},
        )


class TransactionNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "data": None, "details": "Transaction not found"},
        )


class AssetNotAvailable(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "error", "data": None, "details": "Asset not available"},
        )


class TransactionsAccessForbidden(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"status": "error", "data": None, "details": "Access to the user's transactions is forbidden"},
        )


class InsufficientFunds(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={"status": "error", "data": None, "details": "Not enough balance to buy asset"},
        )
