from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_session
from app.db import models
from app.services.user.service import UserService
from app.db.repositories.user_repo import UserRepository
from app.schemas.token import TokenSchema
from app.utils.jwt_auth0 import VerifyToken
from app.schemas.user import (
    UserDetail,
    SignUpRequest,
    SignInRequest,
    UserUpdateRequest,
    UserDeletedResponse,
    UserSummary,
)


router = APIRouter(prefix="/users")
auth0 = VerifyToken()


async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(models.User, db)
    return UserService(repo=user_repository)


@router.get("/", response_model=List[UserSummary])
async def read_users(
    user_service: UserService = Depends(get_user_service),
    skip: int = 0,
    limit: int = 100,
):
    """Get all users"""
    return await user_service.get_user_list(skip, limit)


@router.get("/me", response_model=UserDetail)
async def read_current_user(
    token: str, user_service: UserService = Depends(get_user_service)
):
    """Get a user by token"""
    return await user_service.get_current_user(token=token)


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """Get a user by ID."""
    return await user_service.get_user(id=user_id)


@router.post("/", response_model=UserDetail)
async def create_new_user(
    user_data: SignUpRequest, user_service: UserService = Depends(get_user_service)
):
    """Create a new user (Sign Up)."""
    return await user_service.create_user(data=user_data)


@router.post("/signin", response_model=TokenSchema)
async def signin(
    data: SignInRequest, user_service: UserService = Depends(get_user_service)
):
    """User sign in"""
    return await user_service.signin_user(data=data)


@router.post("/auth0")
async def auth0_signin(
    auth_result: str = Security(auth0.verify),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.signin_auth0_user(auth_result)


@router.put("/{user_id}", response_model=UserDetail)
async def update_existing_user(
    user_id: int,
    user_data: UserUpdateRequest,
    user_service: UserService = Depends(get_user_service),
):
    """Update an existing user."""
    return await user_service.update_user(id=user_id, data=user_data)


@router.delete("/{user_id}", response_model=UserDeletedResponse)
async def delete_existing_user(
    user_id: int, user_service: UserService = Depends(get_user_service)
):
    """Delete an existing user."""
    return await user_service.delete_user(id=user_id)
