from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"status": "error", "data": None, "details": "User not found"}
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


class InsufficientFunds(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={"status": "error", "data": None, "details": "Not enough balance to buy selected asset amount"},
        )


class InsufficientAssets(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "data": None, "details": "You own fewer assets than you are trying to sell."},
        )
