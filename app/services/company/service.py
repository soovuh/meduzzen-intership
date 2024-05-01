from typing import List

from app.db.repositories.company_repo import CompanyRepository
from app.services.shared import base_exceptions
from app.db import models
from app.services.company import exc
from app.schemas.company import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
    DeleteCompanyResponse,
    CompanyDetail,
    CompanyChangeVisibilityRequest,
)


class CompanyService:
    def __init__(self, repo: CompanyRepository) -> None:
        self._repo = repo

    async def get_companies_list(
        self, skip: int = 0, limit: int = 100
    ) -> List[models.Company]:
        companies = await self._repo.get_public_list(skip, limit)
        return companies

    async def get_company(self, id: int) -> CompanyDetail:
        company: models.Company | None = await self._repo.get(id)

        if company is None or company.is_hidden:
            raise exc.CompanyNotFound(identifier=id)

        return company

    async def create_company(
        self, data: CreateCompanyRequest, user: models.User
    ) -> models.Company:
        data_dict = data.model_dump()
        data_dict["owner_id"] = user.id

        company = await self._repo.create(data=data_dict)

        if company is None:
            raise exc.CompanyCreateError()

        return company

    async def update_company(
        self, id: int, data: UpdateCompanyRequest, user: models.User
    ) -> models.Company:
        company: models.Company | None = await self._repo.get(id)

        if company is None:
            raise exc.CompanyNotFound(identifier=id)

        if not user.id == company.owner_id:
            raise exc.CompanyAccessError()

        data_dict = data.model_dump()

        if not data.name:
            del data_dict["name"]
        if not data.description:
            del data_dict["description"]

        company = await self._repo.update(id=id, data=data_dict)

        return company

    async def change_visibility(
        self, id: int, data: CompanyChangeVisibilityRequest, user: models.User
    ):
        company: models.Company | None = await self._repo.get(id)

        if company is None:
            raise exc.CompanyNotFound(identifier=id)

        if not user.id == company.owner_id:
            raise exc.CompanyAccessError()

        company = await self._repo.update(id=id, data=data.model_dump())

        return company

    async def delete_company(self, id: int, user: models.User) -> models.Company:
        company: models.Company = await self._repo.get(id)

        if company is None:
            raise exc.CompanyNotFound(identifier=id)

        if not user.id == company.owner_id:
            raise exc.CompanyAccessError()

        deleted = await self._repo.delete(id)

        if deleted is False:
            raise exc.CompanyNotFound(identifier=id)

        return DeleteCompanyResponse()
