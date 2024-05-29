from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class CompanyDetail(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    is_hidden: bool


class CreateCompanyRequest(BaseModel):
    name: str
    description: str
    is_hidden: Optional[bool] = False


class UpdateCompanyRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CompanySummary(BaseModel):
    id: int
    name: str


class CompanyChangeVisibilityRequest(BaseModel):
    is_hidden: bool


class DeleteCompanyResponse(BaseModel):
    result: str = "company has been successfully deleted"
