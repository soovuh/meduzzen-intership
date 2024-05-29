from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.routers.user import get_active_user
from app.db import models
from app.db.database import get_session
from app.services.company.service import CompanyService
from app.db.repositories.company_repo import CompanyRepository
from app.schemas.company import (
    CompanyDetail,
    CreateCompanyRequest,
    UpdateCompanyRequest,
    DeleteCompanyResponse,
    CompanySummary,
    CompanyChangeVisibilityRequest,
)

router = APIRouter(prefix="/company")


async def get_company_service(
    db: AsyncSession = Depends(get_session),
) -> CompanyService:
    company_repository = CompanyRepository(models.Company, db)
    return CompanyService(repo=company_repository)


@router.get("/", response_model=List[CompanySummary])
async def read_companies(
    company_service: CompanyService = Depends(get_company_service),
    skip: int = 0,
    limit: int = 100,
):
    """Get all companies"""
    return await company_service.get_companies_list(skip, limit)


@router.put("/change_visibility/{company_id}", response_model=CompanyDetail)
async def change_visibility(
    company_id: int,
    data: CompanyChangeVisibilityRequest,
    company_service: CompanyService = Depends(get_company_service),
    current_user: models.User = Depends(get_active_user),
):
    """Change visibility"""
    return await company_service.change_visibility(company_id, data, current_user)


@router.get("/{company_id}", response_model=CompanyDetail)
async def read_company(
    company_id: int,
    company_service: CompanyService = Depends(get_company_service),
):
    """Get company by id"""
    return await company_service.get_company(company_id)


@router.post("/", response_model=CompanyDetail)
async def create_new_company(
    company_data: CreateCompanyRequest,
    current_user: models.User = Depends(get_active_user),
    company_service: CompanyService = Depends(get_company_service),
):
    """Create new company"""
    return await company_service.create_company(company_data, current_user)


@router.put("/{company_id}", response_model=CompanyDetail)
async def update_existing_company(
    company_id: int,
    company_data: UpdateCompanyRequest,
    current_user: models.User = Depends(get_active_user),
    company_service: CompanyService = Depends(get_company_service),
):
    """Update existing company"""
    return await company_service.update_company(company_id, company_data, current_user)


@router.delete("/{company_id}", response_model=DeleteCompanyResponse)
async def delete_company(
    company_id: int,
    current_user: models.User = Depends(get_active_user),
    company_service: CompanyService = Depends(get_company_service),
):
    """Delete company"""
    return await company_service.delete_company(company_id, current_user)
