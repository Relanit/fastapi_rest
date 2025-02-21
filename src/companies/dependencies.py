from typing import Annotated

from fastapi import Depends

from companies.exceptions import CompanyNotFound
from companies.service import CompanyService
from models import Company

CompanyServiceDep = Annotated[CompanyService, Depends(CompanyService)]


async def valid_company_id(company_id: int, service: CompanyServiceDep) -> Company:
    company = await service.get_by_id(company_id)
    if not company:
        raise CompanyNotFound()
    return company
