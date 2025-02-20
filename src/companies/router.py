from fastapi import APIRouter, Depends
from fastapi import status

from auth.auth import current_user_admin
from companies.dependencies import valid_company_id, CompanyServiceDep
from companies.schemas import CompanyCreate, CompanyUpdate, CompanyResponse, CompanyPatchUpdate
from models import Company
from pagination import PaginatorDep

router = APIRouter(prefix="/companies", tags=["Company"])


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    service: CompanyServiceDep,
    current_user_admin=Depends(current_user_admin),
):
    created_company = await service.create(company)
    return created_company


@router.get("/", response_model=list[CompanyResponse], status_code=status.HTTP_200_OK)
async def get_companies(pagination: PaginatorDep, service: CompanyServiceDep):
    companies = await service.get_all(pagination.limit, pagination.skip)
    return companies


@router.get("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def get_specific_company(company: Company = Depends(valid_company_id)):
    return company


@router.put("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def update_company(
    updated_company: CompanyUpdate,
    service: CompanyServiceDep,
    company: Company = Depends(valid_company_id),
    current_user_admin=Depends(current_user_admin),
):
    company_updated = await service.update_full(company, updated_company)
    return company_updated


@router.patch("/{company_id}", response_model=CompanyResponse, status_code=status.HTTP_200_OK)
async def partial_update_company(
    company_data: CompanyPatchUpdate,
    service: CompanyServiceDep,
    company: Company = Depends(valid_company_id),
    current_user_admin=Depends(current_user_admin),
):
    updated_company = await service.update_partial(company, company_data)
    return updated_company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    service: CompanyServiceDep,
    company: Company = Depends(valid_company_id),
    current_user_admin=Depends(current_user_admin),
):
    await service.delete(company)
