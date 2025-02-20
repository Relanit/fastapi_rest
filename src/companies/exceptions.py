from fastapi import HTTPException, status


class CompanyAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "data": None, "details": "Company already exists"},
        )


class CompanyNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "data": None, "details": "Company not found"},
        )
