from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db import models
from app.services.user.service import UserService
from app.db.repositories.user_repo import UserRepository
from app.schemas.user import (
    UsersListResponse,
    UserDetail,
    SignUpRequest,
    UserUpdateRequest,
)


router = APIRouter(prefix="/users")


async def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    user_repository = UserRepository(models.User, db)
    return UserService(repo=user_repository)


@router.get("/", response_model=UsersListResponse)
async def read_users(
    user_service: UserService = Depends(get_user_service), skip: int = 0, limit: int = 100
):
    """Get all users"""
    return await user_service.get_user_list(skip, limit)


@router.get("/{user_id}", response_model=UserDetail)
async def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Get a user by ID."""
    return await user_service.get_user(id=user_id)



@router.post("/", response_model=UserDetail)
async def create_new_user(
    user_data: SignUpRequest, user_service: UserService = Depends(get_user_service)
):
    """Create a new user (Sign Up)."""
    return await user_service.create_user(data=user_data)


@router.put("/{user_id}", response_model=UserDetail)
async def update_existing_user(
    user_id: int, user_data: UserUpdateRequest, user_service: UserService = Depends(get_user_service)
):
    """Update an existing user."""
    return await user_service.update_user(id=user_id, data=user_data)


@router.delete("/{user_id}", response_model=dict)
async def delete_existing_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Delete an existing user."""
    return await user_service.delete_user(id=user_id)
