from fastapi import HTTPException, status


class AssetNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "data": None, "details": "Asset not found"},
        )
