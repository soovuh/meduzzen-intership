from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserDetail(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    name: Optional[str]
    password: Optional[str]


class UserDetailResponse(BaseModel):
    user: UserDetail


class UsersListResponse(BaseModel):
    users: List[UserDetail]
